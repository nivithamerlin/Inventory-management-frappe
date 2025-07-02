import frappe
def execute(filters=None):
   columns = [
      {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 120},
      {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
      {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 100},
      {"label": "Stock Qty", "fieldname": "stock_qty", "fieldtype": "int", "width": 100},
      {"label": "Reorder Level", "fieldname": "reorder_level", "fieldtype": "int", "width": 100},
      {"label": "Reorder Needed?", "fieldname": "reorder_required", "fieldtype": "Data", "width": 120},
   ]
   items = frappe.get_all("Item", fields=["item_code", "item_name", "category", "stock_qty", "reorder_level"])
   data = []
   for item in items:
      reorder_required = "Yes" if (item.stock_qty or 0) < (item.reorder_level or 0) else "No"
      data.append({
         "item_code": item.item_code,
         "item_name": item.item_name,
         "category": item.category,
         "stock_qty": item.stock_qty,
         "reorder_level": item.reorder_level,
         "reorder_required": reorder_required
      })
   return columns, data