import frappe
def execute(filters=None):
    columns = [
		{"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Int", "width": 100},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data", "width": 120}
	]
    data = []
    entries  = frappe.get_all(
		"Sales Order",
		fields = ["item", "quantity", "date", "customer"],
  		order_by = "date desc"
		)
    for entry in entries:
        data.append({
			"item": entry.item,
   			"quantity": entry.quantity,
      		"date": entry.date,	
         	"customer": entry.customer,	
		})
    return columns, data
        
    