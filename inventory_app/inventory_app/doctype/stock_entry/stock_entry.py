def validate(self):
    if self.quantity is None or self.quantity <= 0:
        frappe.throw("Quantity must be greater than 0")

    