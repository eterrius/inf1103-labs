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

    def validate_stock(self) -> bool:
        if self.__stock < 0:
            raise ValueError(
                f"Invalid quantity for product {self.get_product_info()['name']}. Quantity must be greater than 0."
            )

    def validate_price(self) -> bool:
        if self.__price <= 0:
            raise ValueError(
                f"Invalid price for product {self.get_product_info()['name']}. Price must be greater than 0."
            )
