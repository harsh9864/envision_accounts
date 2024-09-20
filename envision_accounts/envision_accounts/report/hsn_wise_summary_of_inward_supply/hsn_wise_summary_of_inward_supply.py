# Copyright (c) 2024, Dhruvil Mistry and contributors
# For license information, please see license.txt

import frappe
from typing import List, Dict, Any

def execute(filters=None):
	columns: List[Dict[str, Any]] = get_columns()
	data: List[Dict[str, Any]] = get_data(filters)
	return columns, data

def get_columns() -> List[Dict[str, Any]]:
	return [
    {
		"label": "<b>GST HSN Code</b>",
		"fieldname": "HSN",
		"fieldtype": "Link",
		"options": "GST HSN Code",
	},
    {
        "label": "<b>Description</b>",
        "fieldname": "Description",
		"fieldtype": "Data",
	},
	{
		"label": "<b>UOM</b>",
		"fieldname": "UOM",
		"fieldtype": "Link",
		"options": "UOM"
    },
	{
		"label": "<b>GST UOM</b>",
		"fieldname": "GST UOM",
		"fieldtype": "Data",
    },
	{
		"label": "<b>Total Quantity</b>",
		"fieldname": "Total Quantity",
		"fieldtype": "Float",
		"precision":2
    },
	{
		"label": "<b>Total Taxable Value</b>",
		"fieldname": "Total Taxable Value",
		"fieldtype": "Float",
		"precision":2
    },
	{
		"label": "<b>Integrated Tax</b>",
		"fieldname": "Integrated Tax",
		"fieldtype": "Float",
		"precision":2
    },
	{
		"label": "<b>Central Tax</b>",
		"fieldname": "Central Tax",
		"fieldtype": "Float",
		"precision":2
    },
	{
		"label": "<b>State/UT Tax</b>",
		"fieldname": "State/UT Tax",
		"fieldtype": "Float",
		"precision":2
    },
	{
		"label": "<b>Cess Amount</b>",
		"fieldname": "Cess Amount",
		"fieldtype": "Float",
		"precision":2
    },
    ]

def get_data(filters=None) -> List[Dict[str, Any]]:
	result_data_sql: str = """
	SELECT 
		PII.gst_hsn_code AS "HSN",
		PII.description AS "Description",
		PII.qty AS "Total Quantity",
		PII.base_net_rate AS "Total Taxable Value",
		PI.itc_integrated_tax AS "Integrated Tax",
		PI.itc_central_tax AS "Central Tax",
		PI.itc_state_tax AS "State/UT Tax",
		PI.itc_cess_amount AS "Cess Amount",
		PII.stock_uom AS "UOM",
		CONCAT(PII.stock_uom, " - ", GUM.gst_uom) AS "GST UOM",
		CASE 
			WHEN PI.itc_integrated_tax != 0 THEN ROUND((PI.itc_integrated_tax * 100 / PI.net_total),2)
			WHEN PI.itc_integrated_tax = 0 THEN ROUND(((PI.itc_central_tax + PI.itc_state_tax) * 100 / PI.net_total),2)
			ELSE "-"
		END AS "Tax Rate"
	FROM `tabPurchase Invoice Item` AS PII
	INNER JOIN `tabPurchase Invoice` AS PI ON PI.name = PII.parent
	INNER JOIN `tabGST UOM Map` AS GUM ON PII.stock_uom = GUM.uom
	WHERE PI.docstatus = 1
	"""
	if filters.get('from_date') and filters.get('to_date'):
		result_data_sql += f"AND DATE(PI.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
	if filters.get('company'):
		result_data_sql += f" AND PI.company = '{filters.get('company')}'"
	if filters.get('hsn_code'):
		result_data_sql += f" AND PII.gst_hsn_code = '{filters.get('hsn_code')}'"
	result: List[Dict[str, Any]] = frappe.db.sql(result_data_sql,as_dict = 1)
	return result