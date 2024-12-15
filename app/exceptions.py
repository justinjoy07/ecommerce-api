class InsufficientStockError(Exception):
    """
    Raised when order quantity exceeds available product stock.
    """
    def __init__(self, product_id, requested_quantity, available_stock):
        self.product_id = product_id
        self.requested_quantity = requested_quantity
        self.available_stock = available_stock
        self.message = (f"Insufficient stock for product {product_id}. "
                        f"Requested: {requested_quantity}, "
                        f"Available: {available_stock}")
        super().__init__(self.message)

class ProductValidationError(Exception):
    """
    Raised when product data is invalid.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)