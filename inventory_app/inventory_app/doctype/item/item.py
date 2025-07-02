import frappe
from frappe.model.document import Document

class Item(Document):
    def validate(self):
        if self.reorder_level:
            stock_qty = get_stock_balance(self.item_code, self.stock_qty or 0)
            if stock_qty < self.reorder_level:
                frappe.sendmail(
                    recipients=["nivithamerlin@gmail.com"],
                    subject=f"Reorder Alert: {self.item_name}",
                    message = f"""
						<p>The stock for <strong>{self.item_name}</strong> has dropped to {stock_qty},
                        which is below the reorder level of {self.reorder_level}.</p>
                        <p>Please restock as soon as possible.</p>"
                    """
                )

def get_stock_balance(item_code, fallback_stock_qty):
    total_in = frappe.db.sql("""
        SELECT SUM(quantity) FROM `tabStock Entry`
        WHERE item = %s AND type = 'In'
    """, (item_code,))[0][0] or 0
    total_out = frappe.db.sql("""
        SELECT SUM(quantity) FROM `tabStock Entry`
        WHERE item = %s AND type = 'Out'
    """, (item_code,))[0][0] or 0
    if total_in == 0 and total_out == 0:
        return fallback_stock_qty
    return total_in - total_out