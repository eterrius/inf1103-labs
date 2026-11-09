# --- Imports --- #
from product import Product
from supplier import Supplier


# --- Classes --- #
class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        type: str,
        name: str,
        price: float,
        stock: int,
        download_size: float,
        supplier: Supplier,
    ):
        super().__init__(product_id, type, name, price, stock, supplier)
        self.__download_size = download_size

    def display_information(self):
        product_info = super().get_product_info()
        product_info["download_size"] = self.__download_size
        return product_info

    def get_fulfilment_info(self):
        return f"This product is delivered digitally."
