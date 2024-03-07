// Copyright (c) 2024, Rucha Mahabal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Member", {
	refresh(frm) {
		frm.trigger("add_custom_buttons");
	},

	add_custom_buttons(frm) {
		frm.add_custom_button(
			__("Membership"),
			() => {
				frappe.new_doc("Library Membership", {
					member: frm.doc.name,
				});
			},
			__("Create")
		);

		frm.add_custom_button(
			__("Transaction"),
			() => {
				frappe.new_doc("Library Transaction", {
					member: frm.doc.name,
				});
			},
			__("Create")
		);
	},
});
