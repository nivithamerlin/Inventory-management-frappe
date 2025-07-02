import frappe
def execute(filters=None):
    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Int", "width": 100},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 200},
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 120}
    ]
    data = []
    entries = frappe.get_all(
        "Stock Entry",
        fields = ["item", "quantity", "date", "category", "supplier"],
        filters={"type": "In"},
        order_by = "date desc"
        )
    for entry in entries:
        data.append({
            "item": entry.item,
            "quantity": entry.quantity,
            "date": entry.date,
            "category": entry.category,
            "supplier": entry.supplier
        })
    return columns, data