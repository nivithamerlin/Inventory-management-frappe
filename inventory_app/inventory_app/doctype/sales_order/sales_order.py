import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
class SalesOrder(Document):
    def on_submit(self):
        # Create a Stock Ledger entry for Sales
        ledger_entry = frappe.get_doc({
            "doctype": "Stock Ledger",
            "item": self.item,
            "warehouse": self.warehouse,
            "quantity": -self.quantity,  # Stock goes OUT
            "type": "Sales",
            "date": self.date or nowdate()
        })
        ledger_entry.insert()
        frappe.msgprint("Stock Ledger updated for Sales")
