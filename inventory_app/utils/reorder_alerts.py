import frappe
def check_reorder_levels():
    items = frappe.get_all("Item", fields=["item_name", "item_code", "reorder_level", "stock_qty"])
    for item in items:
        if item.reorder_level is not None:
            stock_qty = get_stock_balance(item.item_code, item.stock_qty or 0)
            if stock_qty < item.reorder_level:
                send_reorder_email(item, stock_qty)
                
def get_stock_balance(item_code, fallback_stock_qty):
    # calculate stock from stock entry
    total_in = frappe.db.sql("""
        SELECT SUM(quantity) FROM `tabStock Entry`
        WHERE item = %s AND type = 'In'
    """, (item_code,))[0][0] or 0
    total_out = frappe.db.sql("""
        SELECT SUM(quantity) FROM `tabStock Entry`
        WHERE item = %s AND type = 'Out'
    """, (item_code,))[0][0] or 0
    stock_entry_qty = total_in - total_out

# if no stock entry exists, fall back to Items stock quantity field
    if (total_in == 0 and total_out == 0):
        return fallback_stock_qty
    else:
        return stock_entry_qty
    
def send_reorder_email(item, stock_qty):
    restock_qty = item.reorder_level - stock_qty
    frappe.sendmail(
        recipients=["nivithamerlin@gmail.com"],
        subject=f"Reorder Alert: {item.item_name}",
        message = f"""
            <p>The stock for <strong>{item.item_name}</strong> has dropped to {stock_qty}, 
            which is below the reorder level of {item.reorder_level}.</p>
            <p>Please restock atleast <strong>{restock_qty}</strong> units.</p>
        """
)
