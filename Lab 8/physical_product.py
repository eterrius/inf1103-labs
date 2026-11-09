# --- Imports --- #
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


# --- Classes --- #
class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: str,
        type: str,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier,
    ):
        super().__init__(product_id, type, name, price, stock, supplier)
        self.__weight = weight

    def display_information(self):
        product_info = super().get_product_info()
        product_info["weight"] = self.__weight
        return product_info

    def get_fulfilment_info(self):
        return f"This product requires physical shipping."

    def calculate_shipping_cost(self):
        shipping_cost_per_kg = 5.0  # Example shipping cost per kg
        return self.__weight * shipping_cost_per_kg
