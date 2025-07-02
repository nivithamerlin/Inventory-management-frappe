# Copyright (c) 2025, nivitha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockEntry(Document):
    def before_submit(self):
        item = frappe.get_doc("Item", self.item)
        current_stock = item.stock_qty or 0
        if self.type == "In":
            item.stock_qty = current_stock + self.quantity
        elif self.type == "Out":
            if current_stock < self.quantity:
                frappe.throw("Not enough stock to remove")
            item.stock_qty = current_stock - self.quantity
        item.save()
        
    def validate(self):
        if self.quantity is None or self.quantity <= 0:
            frappe.throw("Quantity must be greater than 0")