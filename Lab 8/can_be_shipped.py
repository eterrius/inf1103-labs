# --- Imports --- #
from abc import ABC, abstractmethod


# --- Classes --- #
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
