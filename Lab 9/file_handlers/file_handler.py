# --- Imports --- #
from abc import ABC, abstractmethod
from inventory import Inventory


# --- Classes --- #
class FileHandler(ABC):
    def __init__(self, inventory: Inventory, filename: str):
        self.__filename = filename
        self._inventory = inventory

    @abstractmethod
    def load_inventory(self) -> dict:
        pass

    @abstractmethod
    def save_inventory(self) -> None:
        pass
