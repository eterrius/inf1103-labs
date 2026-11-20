# --- Imports --- #
from products import Product


# --- Classes --- #
class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_product_info()["price"] * self.quantity

    def validate_quantity(self) -> bool:
        if self.quantity <= 0:
            raise ValueError(
                f"Invalid quantity for product {self.product.get_product_info()['name']}. Quantity must be greater than 0."
            )

        if self.quantity > self.product.get_product_info()["stock"]:
            raise ValueError(
                f"Insufficient stock for product {self.product.get_product_info()['name']}. Available stock: {self.product.get_product_info()['stock']}."
            )
