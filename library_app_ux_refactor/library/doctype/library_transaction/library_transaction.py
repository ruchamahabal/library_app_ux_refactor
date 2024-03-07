# Copyright (c) 2024, Rucha Mahabal and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, date_diff, get_link_to_form, getdate


class LibraryTransaction(Document):
	def validate(self):
		if not frappe.db.get_value(
			"Library Membership",
			{
				"member": self.member,
				"from_date": ("<=", self.transaction_date),
				"to_date": (">=", self.transaction_date),
			},
		):
			frappe.throw(_("No active membership"))

	@frappe.whitelist()
	def reissue_book(self):
		if self.transaction_type == "Returned":
			frappe.throw(_("Cannot reissue returned book"))

		doc = frappe.copy_doc(self)
		doc.update(
			{
				"transaction_type": "Issue",
				"transaction_date": self.transaction_date,
				"due_date": add_days(self.due_date, 7),
				"reissued": 1,
				"reissued_from": self.name,
				"remarks": _("Reissued from {0}").format(self.name),
			}
		)
		doc.insert()

		self.status = "Reissued"
		self.save()

		frappe.msgprint(
			_("Book reissued successfully: {0}").format(get_link_to_form(doc.doctype, doc.name)),
			title=_("Success"),
			indicator="green",
		)

	@frappe.whitelist()
	def return_book(self):
		if self.transaction_type == "Returned":
			frappe.throw(_("Book is already returned"), title=_("Not Allowed"))

		self.transaction_type = "Returned"
		self.return_date = getdate()
		self.save()

		frappe.msgprint(
			_("Book returned successfully"),
			title=_("Success"),
			indicator="green",
		)

	@frappe.whitelist()
	def send_receipt(self):
		frappe.sendmail(
			recipients=self.member_email,
			subject=_("Library Transaction Receipt"),
			message=_("You issued the book {0} on {1}").format(self.book, self.transaction_date),
			attachments=[
				frappe.attach_print(self.doctype, self.name, file_name=self.name),
			],
		)

		frappe.msgprint(
			_("Receipt sent successfully to {0}").format(self.member_email),
			title=_("Success"),
			indicator="green",
		)

	@frappe.whitelist()
	def charge_fine(self):
		if self.transaction_type != "Returned":
			frappe.throw(_("Fine can be charged only for returned books"))

		if self.return_date <= self.due_date:
			frappe.throw(_("No fine applicable"))

		overdue_fine = frappe.db.get_single_value("Library Settings", "overdue_fine")
		if not overdue_fine:
			frappe.throw(
				_("Please set the {0} in {1}").format(
					_("Overdue Fine per Day"), get_link_to_form("Library Settings", "Library Settings")
				),
				title=_("Missing Setup"),
			)

		doc = frappe.new_doc("Library Fine")
		doc.update(
			{
				"member": self.member,
				"library_transaction": self.name,
				"fine_amount": (date_diff(self.due_date, self.due_date) + 1) * overdue_fine,
			}
		)
		doc.insert()

		frappe.msgprint(
			_("Library Fine created successfully: {0}").format(get_link_to_form(doc.doctype, doc.name)),
			title=_("Success"),
			indicator="green",
		)
