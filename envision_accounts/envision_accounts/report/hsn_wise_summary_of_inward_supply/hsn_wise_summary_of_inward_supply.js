// Copyright (c) 2024, Dhruvil Mistry and contributors
// For license information, please see license.txt

frappe.query_reports["HSN-wise-Summary of Inward Supply"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": (frappe.datetime.add_months(frappe.datetime.get_today(), -1)),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "hsn_code",
			"label": __("GST HSN Code"),
			"fieldtype": "Link",
			"options": "GST HSN Code",
		},
	]
};
