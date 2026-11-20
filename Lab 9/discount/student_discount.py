# --- Imports --- #
from .discount_strategy import DiscountStrategy


# --- Classes --- #
class StudentDiscount(DiscountStrategy):
    def __init__(self, discount_amount: float = 0.05):
        self.discount_amount = discount_amount

    def apply(self, total: float) -> float:
        return total * (1 - self.discount_amount)
