# Copyright (c) 2024, Dhruvil Mistry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HCFManagement(Document):
	pass

@frappe.whitelist()
def send_email_to_contact(email):
    try:
        
        frappe.sendmail(
            recipients=[email],
            subject="Your Email Subject",
            message="Hello, this is the email body content.",
            now = True
        )
        return True
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Failed to send email')
        return False

@frappe.whitelist()
def filtering_address():
    customer = frappe.form_dict.get('customer')  # Use get() for safer access
    address_filtering_sql = f"""
        SELECT 
            parent
        FROM `tabDynamic Link`
        WHERE link_name = "{customer}"
        AND link_doctype = "Customer"
        AND parenttype = "Address"
    """
    
    addresses = frappe.db.sql(address_filtering_sql, as_dict=True)
    frappe.response["data"] = addresses


