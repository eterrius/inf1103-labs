# --- Imports ---
from abc import ABC, abstractmethod


# --- Classes --- #
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass
