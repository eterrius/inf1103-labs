# --- Imports --- #
from product import Product
from order_line import OrderLine
from discount import DiscountStrategy, NoDiscount


# --- Classes --- #
class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy = None):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount else NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount