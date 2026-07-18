"""Thin wrappers around Frappe APIs used by consignment application services."""


def get_list(doctype, fields=None, filters=None, order_by=None, limit_page_length=None):
	import frappe

	kwargs = {
		"fields": fields or [],
		"filters": filters or {},
	}
	if order_by is not None:
		kwargs["order_by"] = order_by
	if limit_page_length is not None:
		kwargs["limit_page_length"] = limit_page_length

	return frappe.get_list(doctype, **kwargs)


def get_doc(*args, **kwargs):
	import frappe

	return frappe.get_doc(*args, **kwargs)


def db_get_value(doctype, name, fieldname):
	import frappe

	return frappe.db.get_value(doctype, name, fieldname)


def db_set_value(doctype, name, fieldname, value):
	import frappe

	return frappe.db.set_value(doctype, name, fieldname, value)


def throw(message):
	import frappe

	frappe.throw(message)
