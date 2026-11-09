# --- Imports --- #
from abc import ABC, abstractmethod
from supplier import Supplier


# --- Classes --- #
class Product(ABC):
    def __init__(
        self,
        product_id: str,
        type: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ):
        self.__product_id = product_id
        self.__type = type
        self.__name = name
        self.__price = price
        self.__stock = stock

        self.supplier: Supplier = supplier

    def update_stock(self, new_stock: int) -> None:
        self.__stock = new_stock

    def get_product_info(self) -> dict:
        return {
            "product_id": self.__product_id,
            "type": self.__type,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.display_information(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
