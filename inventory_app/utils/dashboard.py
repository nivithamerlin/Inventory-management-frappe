# inventory_app/utils/dashboard.py
import frappe
@frappe.whitelist()
def get_total_stock_value():
    items = frappe.get_all("Item", fields=["stock_qty", "price"])
    total = sum((i.stock_qty or 0) * (i.price or 0) for i in items)
    return {"value": total, "fieldtype": "Currency"}
@frappe.whitelist()
def get_items_below_reorder():
    res = frappe.db.count("Item", filters={
        "stock_qty": ["<", "reorder_level"]
    })
    return {"value": res, "fieldtype": "Int"}
from datetime import datetime, timedelta
@frappe.whitelist()
def get_recent_stock_entries():
    one_week_ago = datetime.now() - timedelta(days=7)
    res = frappe.db.count("Stock Entry", 
        filters={"creation": [">", one_week_ago]})
    return {"value": res, "fieldtype": "Int"}
