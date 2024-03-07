// Copyright (c) 2024, Rucha Mahabal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
	refresh(frm) {
		frm.trigger("add_custom_buttons");
	},

	add_custom_buttons(frm) {
		frm.add_custom_button(__("Reissue"), () => {
			frm.events.confirm_and_proceed(frm, "reissue_book", __("reissue"));
		});

		frm.add_custom_button(__("Return"), () => {
			frm.events.confirm_and_proceed(frm, "return_book", __("return"));
		});

		frm.add_custom_button(__("Send Receipt"), () => {
			frm.events.confirm_and_proceed(frm, "send_receipt", __("send the receipt"));
		}).addClass("btn-primary");

		frm.add_custom_button(__("Charge Fine"), () => {
			frm.events.confirm_and_proceed(frm, "charge_fine", __("charge fine"));
		});
	},

	confirm_and_proceed(frm, action, message) {
		frappe.confirm(__("Are you sure you want to {0}?", [message.bold()]), () => {
			frm.call(action).then(() => frm.refresh());
		});
	},
});
