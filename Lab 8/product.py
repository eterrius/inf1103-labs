# --- Imports --- #
from abc import ABC, abstractmethod


# --- Classes --- #
class Product(ABC):
    def __init__(self, product_id, type, name, price, stock):
        self.__product_id = product_id
        self.__type = type
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def get_product_info(self):
        return {
            "product_id": self.__product_id,
            "type": self.__type,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass
