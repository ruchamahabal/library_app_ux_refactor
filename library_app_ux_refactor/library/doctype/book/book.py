# Copyright (c) 2024, Rucha Mahabal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Count, CurDate
from frappe.utils import add_days, date_diff, get_timestamp, getdate


class Book(Document):
	pass


def get_timeline_data(doctype: str, name: str) -> dict:
	"""Return timeline data for book from library transactions"""
	Transaction = frappe.qb.DocType("Library Transaction")
	data = (
		frappe.qb.from_(Transaction)
		.select(Transaction.transaction_date, Transaction.return_date, Count("*").as_("count"))
		.where((Transaction.book == name) & (Transaction.transaction_date > CurDate() - Interval(years=1)))
		.groupby(Transaction.transaction_date)
	).run(as_dict=True)

	timeline_data = dict()
	today = getdate()

	for row in data:
		no_of_days = date_diff(row.return_date or today, row.transaction_date) + 1
		for i in range(no_of_days):
			timestamp = get_timestamp(add_days(row.transaction_date, i))
			timeline_data.setdefault(timestamp, 0)
			timeline_data[timestamp] += row.count

	return timeline_data
