import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.setup.utils import get_exchange_rate

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		from erpnext.controllers.accounts_controller import get_default_taxes_and_charges

		sales_invoice = frappe.get_doc(target)

		company_currency = frappe.get_cached_value("Company", sales_invoice.company, "default_currency")

		if company_currency == sales_invoice.currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(
				sales_invoice.currency, company_currency, sales_invoice.transaction_date, args="for_selling"
			)

		sales_invoice.conversion_rate = exchange_rate

		# get default taxes
		taxes = get_default_taxes_and_charges("Sales Taxes and Charges Template", company=sales_invoice.company)
		if taxes.get("taxes"):
			sales_invoice.update(taxes)

		sales_invoice.run_method("set_missing_values")
		sales_invoice.run_method("calculate_taxes_and_totals")
		# if not source.get("items", []):
		# 	quotation.opportunity = source.name

	doclist = get_mapped_doc(
		"Opportunity",
		source_name,
		{
			"Opportunity": {
				"doctype": "Sales Invoice",
				"field_map": {"party_name": "customer", "name": "title"},
			},
			"Opportunity Item": {
				"doctype": "Sales Invoice Item",
				"field_map": {
					"parent": "prevdoc_docname",
					"parenttype": "prevdoc_doctype",
					"uom": "stock_uom",
				},
				"add_if_empty": True,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist