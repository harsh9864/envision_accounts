# Copyright (c) 2024, Sanskar Technolab Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from typing import Tuple,List,Dict,Any


def execute(filters=None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
	"""
    Execute the report with optional filters.

    Args:
        filters (Optional[Dict[str, Any]]): Filters to apply to the report.

    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: A tuple containing the columns
        and data of the report.
    """
    
	columns: List[Dict[str, Any]] = get_columns()
	data: List[Dict[str, Any]] = get_data(filters)
	return columns, data

def get_columns() -> List[Dict[str,Any]]:
    
	"""
    Fetches the columns for the report.

    Returns:
        List[Dict[str,Any]]: Columns of the report.
    """

	columns:  List[Dict[str, Any]] = [
		{
			"fieldname": "posting_date",
			"label": _("<b>Posting Date</b>"),
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"fieldname": "name",
			"label": _("<b>Ref No.</b>"),
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 130,
		},
		{
			"fieldname": "supplier",
			"label": _("<b>Party's Name</b>"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "custom_msme_type",
			"label": _("<b>Type Of Enterprise</b>"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "pan",
			"label": _("<b>PAN / IT No</b>"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "custom_certificate_number",
			"label": _("<b>UDYAM Reg No.</b>"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "grand_total",
			"label": _("<b>Amount Pending after Due Date</b>"),
			"fieldtype": "Float",
			"precision":2,
			"width": 130,
		},
		{
			"fieldname": "due_date",
			"label": _("<b>Due on (As Per MSME)</b>"),
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"fieldname": "credit_days",
			"label": _("<b>Credit Days</b>"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "clearance_date",
			"label": _("<b>Cleared On</b>"),
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"fieldname": "days_till_due_date",
			"label": _("<b>Days till Due Date</b>"),
			"fieldtype": "Int",
			"width": 130,
		},
	]
	return columns

def get_data(filters:dict = None) -> List[Dict[str,Any]]:
	"""Returns the data for the report"""

	sql:str = f"""

	SELECT 
		PI.posting_date, 
		PI.name,
		PI.supplier,
		S.custom_msme_type,
		S.pan,
		S.custom_certificate_number,
		PI.grand_total,
		PI.due_date,
		PTT.credit_days,
		DATE(PE.creation) AS clearance_date,
		CASE
        WHEN DATE(PE.creation) IS NOT NULL THEN
            CASE
                WHEN DATE(PI.due_date) = DATE(PE.creation) THEN 0
                ELSE DATEDIFF(PI.due_date,DATE(PE.creation))
            END
        ELSE DATEDIFF(PI.due_date,CURDATE())
    END AS days_till_due_date
	FROM 
		`tabPurchase Invoice` AS PI 
	INNER JOIN 
		`tabSupplier` AS S ON S.name = PI.supplier
	INNER JOIN 
		`tabPayment Terms Template Detail` AS PTT ON PTT.parent = PI.payment_terms_template
	LEFT JOIN 
		`tabPayment Entry Reference` AS PER ON PER.reference_name = PI.name
	LEFT JOIN
		`tabPayment Entry` AS PE ON PER.parent = PE.name
	WHERE 
		S.custom_is_msme = 1

	"""

	if filters.get('supplier'):
		sql += f" AND PI.supplier = '{filters.get('supplier')}'"

	if filters.get('custom_msme_type'):
		sql += f" AND S.custom_msme_type = '{filters.get('custom_msme_type')}'"

	if filters.get('from_date') and filters.get('to_date'):
		sql += f"AND PI.posting_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"

	result: List[Dict[str, Any]] = frappe.db.sql(sql,as_dict = True)

	return result