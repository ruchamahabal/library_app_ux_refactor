# Copyright (c) 2024, Rucha Mahabal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):
	def validate(self):
		if not frappe.db.get_value(
			"Library Membership",
			{"member": self.member, "from_date": ("<=", self.date), "to_date": (">=", self.date)},
		):
			frappe.throw("No active membership")
