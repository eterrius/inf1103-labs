# --- Imports --- #
from .discount_strategy import DiscountStrategy


# --- Classes --- #
class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total