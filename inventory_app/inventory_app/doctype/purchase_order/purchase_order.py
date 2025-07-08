import frappe
from frappe.model.document import Document
class PurchaseOrder(Document):
    def on_submit(self):
        frappe.get_doc({
			"doctype": "Stock Ledger",
   			"item": self.item,
      		"quantity": self.quantity,
        	"type": "Purchase",
         	"date": self.date,
      		"warehouse": self.warehouse,	
		}).insert()
