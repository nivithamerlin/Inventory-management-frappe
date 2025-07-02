import frappe
from inventory_app.utils.reorder_alert import check_reorder_alerts

def daily_low_stock_summary():
    frappe.log_error("Running daily low stock summary")
    check_reorder_alerts()  # reuse your existing reorder alert logic
