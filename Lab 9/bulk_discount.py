# --- Imports --- #
from .discount_strategy import DiscountStrategy


# --- Classes --- #
class BulkDiscount(DiscountStrategy):
    def __init__(self, discount_amount: float = 20, threshold: int = 200):
        self.__threshold = threshold
        self.__discount_amount = discount_amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__discount_amount
        return total
