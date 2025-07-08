import frappe
def execute(filters=None):
    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Int", "width": 100},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Data", "width": 120}
    ]
    data = []
    entries = frappe.get_all(
        "Purchase Order",
        fields = ["item", "quantity", "date", "supplier"],
        order_by = "date desc"
        )
    for entry in entries:
        data.append({
            "item": entry.item,
            "quantity": entry.quantity,
            "date": entry.date,
            "supplier": entry.supplier
        })
    return columns, data