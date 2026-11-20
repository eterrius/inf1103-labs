# --- Imports --- #
from .discount_strategy import DiscountStrategy


# --- Classes --- #
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 0.9):
        self.__percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage)
