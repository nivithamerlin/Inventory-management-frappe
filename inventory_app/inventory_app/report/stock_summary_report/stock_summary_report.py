import frappe
def execute(filters=None):
   columns = [
      {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 120},
      {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
      {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 100},
      {"label": "Current Stock", "fieldname": "stock_qty", "fieldtype": "int", "width": 100},
      {"label": "Reorder Level", "fieldname": "reorder_level", "fieldtype": "int", "width": 100},
      {"label": "Reorder Needed?", "fieldname": "reorder_required", "fieldtype": "Data", "width": 120},
   ]
   data = []
   items = frappe.get_all("Item", fields=["item_code", "item_name", "category", "stock_qty", "reorder_level"])
   
   for item in items:
      stock_qty = frappe.db.sql("""
            SELECT 
                SUM(CASE 
                        WHEN type = 'Purchase' THEN quantity
                        WHEN type = 'Sales' THEN -quantity
                        ELSE 0
                    END) as qty
            FROM `tabStock Ledger`
            WHERE item = %s
        """, (item.item_code,), as_dict=True)[0].qty or 0
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