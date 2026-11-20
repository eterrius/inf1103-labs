# --- Imports --- #
from products import Product


# --- Classes --- #
class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_product_info()["price"] * self.quantity
