// Copyright (c) 2024, Dhruvil Mistry and contributors
// For license information, please see license.txt

frappe.query_reports["MSME"] = {
		"filters": [
			{
			"fieldname": "company",
			"fieldtype": "Link",
			"label": "Company",
			"mandatory": 0,
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			},
			{
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			},
			{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.get_today()
			},
			{
				"fieldname": "supplier",
				"fieldtype": "Link",
				"label": "Supplier",
				"mandatory": 0,
				"options": "Supplier",
				"get_query": () =>{
					return {
						filters: { "custom_is_msme": "1" }
					}
				},
			},
			{
				"default":" ",
				"fieldname": "custom_msme_type",
				"fieldtype": "Select",
				"label": "Type",
				"options": "\nMicro\nSmall\nMedium"
			},
	]
};
