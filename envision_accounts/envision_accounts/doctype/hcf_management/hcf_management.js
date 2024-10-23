// Copyright (c) 2024, Dhruvil Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("HCF Management", {

    refresh: function(frm) {
        // Call the filtering function on form refresh
        update_address_filters(frm);
    },
    
    membership_id: function(frm) {
        // Call the filtering function when membership_id changes
        update_address_filters(frm);
    },
    before_save: function(frm) {
        let contact_details = frm.doc.contact_details;
    
        contact_details.forEach(data => {
            if (data.send_mail && data.email) {
                console.log(`Sending email to: ${data.email}`);
    
                // Call the server-side method to send the email
                frappe.call({
                    method: "envision_accounts.envision_accounts.doctype.hcf_management.hcf_management.send_email_to_contact",
                    args: {
                        email: data.email  // Pass the email address to the server-side method
                    },
                    callback: function(response) {
                        if (response.message) {
                            frappe.msgprint(`Email sent to ${data.email}`);
                        } else {
                            frappe.msgprint(`Failed to send email to ${data.email}`);
                        }
                    }
                });
            }
        });
    },
    validate: function(frm) {
        // Function to validate address linkage and set detailed address
        function validate_address(address_field, detailed_address_field) {
            if (frm.doc[address_field]) {
                frappe.call({
                    method: "frappe.client.get",
                    args: {
                        doctype: "Address",
                        name: frm.doc[address_field],
                    },
                    async: false,  // Make the frappe call synchronous to block form submission
                    callback: function(response) {
                        if (response.message) {
                            let isLinked = false;  // To check if membership_id is linked

                            if (response.message.links && response.message.links.length > 0) {
                                for (let i = 0; i < response.message.links.length; i++) {
                                    if (response.message.links[i].link_name === frm.doc.membership_id) {
                                        isLinked = true;

                                        // Build the address string
                                        let address = `${response.message.address_line1}\n${response.message.address_line2}\n${response.message.city}, ${response.message.state}\n${response.message.country}\n\nPin Code: ${response.message.pincode}\nGSTIN: ${response.message.gstin}`;

                                        // Set the detailed address field
                                        frm.set_value(detailed_address_field, address);
                                        frm.refresh_field(detailed_address_field);
                                        break;
                                    }
                                }
                            }

                            // If not linked, show error and stop form submission
                            if (!isLinked) {
                                frappe.msgprint({
                                    title: __('Address Not Linked'),
                                    message: `Create the address for <b>${frm.doc.membership_id}</b> member or link it with an existing address.`,
                                    indicator: 'red'
                                });
                                frappe.validated = false;  // Prevent the form from being submitted
                            }
                        }
                    }
                });
            } else {
                // Clear the detailed address field if no address is selected
                frm.set_value(detailed_address_field, null);
                frm.refresh_field(detailed_address_field);
            }
        }

        // Validate both hcfs_address and billing_detailed_address fields
        validate_address("hcfs_address", "hcfs_detailed_address");
        validate_address("billing_address", "billing_detailed_address"); // Fixed the address field for billing
    },

    number_of_general_beds:function(frm){total_no_of_beds(frm)},
    number_of_maternity_beds:function(frm){total_no_of_beds(frm)},
    number_of_icu_beds:function(frm){total_no_of_beds(frm)},
    number_of_nicu_beds:function(frm){total_no_of_beds(frm)},
    number_of_special_beds:function(frm){total_no_of_beds(frm)},
    number_of_other_beds:function(frm){total_no_of_beds(frm)},

});

function total_no_of_beds(frm){
    let total_no_of_beds = frm.doc.number_of_general_beds + frm.doc.number_of_maternity_beds + frm.doc.number_of_icu_beds + frm.doc.number_of_nicu_beds + frm.doc.number_of_special_beds + frm.doc.number_of_other_beds
    frm.set_value("number_of_total_beds", total_no_of_beds)

}

function update_address_filters(frm) {
    frappe.call({
        method: "envision_accounts.envision_accounts.doctype.hcf_management.hcf_management.filtering_address",
        args: {
            customer: frm.doc.membership_id
        },
        callback: function(response) {
            if (response.data && response.data.length > 0) {
                let address_names = response.data.map(item => item.parent);
                
                // Set the query for billing_address field
                frm.set_query("billing_address", function() {
                    return {
                        filters: [
                            ["Address", "name", "in", address_names] 
                        ]
                    };
                });
                
                // Set the query for hcfs_address field
                frm.set_query("hcfs_address", function() {
                    return {
                        filters: [
                            ["Address", "name", "in", address_names]  
                        ]
                    };
                });
            } else {
                frm.set_query("billing_address", function() {
                    return {
                        filters: []  // No filter applied
                    };
                });

                frm.set_query("hcfs_address", function() {
                    return {
                        filters: []  // No filter applied
                    };
                });
            }
        }
    });
}