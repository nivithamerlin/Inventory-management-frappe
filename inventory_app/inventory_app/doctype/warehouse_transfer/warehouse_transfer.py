import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class WarehouseTransfer(Document):
    def on_submit(self):
        frappe.msgprint("Script Triggered from Python")
        frappe.msgprint(f"Item: {self.item}, Qty: {self.quantity}, From: {self.from_warehouse}, To: {self.to_warehouse}")

        # 1. Reduce from from_warehouse
        cursor = frappe.db.sql("""
            UPDATE `tabStock Ledger`
            SET quantity = quantity - %(qty)s
            WHERE item = %(item)s AND warehouse = %(from_wh)s
        """, {
            "qty": self.quantity,
            "item": self.item,
            "from_wh": self.from_warehouse
        }, as_dict=False, debug=True)
		# Get affected rows from the database connection's cursor
        affected_from = frappe.db._cursor.rowcount
        frappe.msgprint(f"FROM Rows affected: {affected_from}")
        if affected_from == 0:
            out_entry = frappe.get_doc({
                "doctype": "Stock Ledger",
                "item": self.item,
                "warehouse": self.from_warehouse,
                "quantity": -self.quantity,
                "date": nowdate(),
                "type": "Out"
            })
            out_entry.insert()
            frappe.msgprint("OUT entry created")
            
        # Fetch and show remaining stock in source warehouse
        remaining_from = frappe.db.sql("""
            SELECT SUM(quantity) FROM `tabStock Ledger`
            WHERE item = %s AND warehouse = %s
        """, (self.item, self.from_warehouse))[0][0] or 0
        frappe.msgprint(f"Remaining stock in {self.from_warehouse}: {remaining_from}")

        # 2. Add to to_warehouse
        cursor = frappe.db.sql("""
            UPDATE `tabStock Ledger`
            SET quantity = quantity + %(qty)s
            WHERE item = %(item)s AND warehouse = %(to_wh)s
        """, {
            "qty": self.quantity,
            "item": self.item,
            "to_wh": self.to_warehouse
        }, as_dict=False, debug=True)
        affected_to = frappe.db._cursor.rowcount
        frappe.msgprint(f"TO Rows affected: {affected_to}")
        if affected_to == 0:
            in_entry = frappe.get_doc({
                "doctype": "Stock Ledger",
                "item": self.item,
                "warehouse": self.to_warehouse,
                "quantity": self.quantity,
                "date": nowdate(),
                "type": "In"
            })
            in_entry.insert()
            frappe.msgprint("IN entry created")
            
        # Fetch and show remaining stock in target warehouse
        remaining_to = frappe.db.sql("""
            SELECT SUM(quantity) FROM `tabStock Ledger`
            WHERE item = %s AND warehouse = %s
    	""", (self.item, self.to_warehouse))[0][0] or 0
        frappe.msgprint(f"Current stock in {self.to_warehouse}: {remaining_to}")

        frappe.db.commit()
        frappe.msgprint("Stock Ledger updated successfully.")
