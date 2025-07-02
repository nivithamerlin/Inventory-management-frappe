import frappe
def execute(filters=None):
    columns = [
		{"label": "Item", "fieldname": "item", "fieldtype": "Data", "width": 120},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Data", "width": 150},
        {"label": "Type", "fieldname": "type", "fieldtype": "Select", "width": 200},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Int", "width": 120},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
    ]
    
    # Prepare filters for stock entry
    entry_filters = {}
    if filters and filters.get("warehouse"):
        entry_filters["warehouse"] = filters["warehouse"]
        
    # Fetch entries from stock ledger doctype
    entries = frappe.get_all(
        "Stock Ledger",
        fields=["item", "warehouse", "type", "quantity", "date"],
        filters=entry_filters,
        order_by="date desc"
    )
    data = []
    
    # Process each entry
    for entry in entries:
        qty = entry.quantity if entry.type == "In" else -entry.quantity
        data.append({
            "item": entry.item,
            "warehouse": entry.warehouse,
            "type": entry.type,
            "quantity": qty,
            "date": entry.date
        })
   
    return columns, data