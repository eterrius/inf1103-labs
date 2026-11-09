# --- Imports --- #
from product import Product


# --- Classes --- #
class DigitalProduct(Product):
    def __init__(self, product_id, type, name, price, stock, download_size):
        super().__init__(product_id, type, name, price, stock)
        self.__download_size = download_size

    def display_information(self):
        product_info = super().get_product_info()
        product_info["download_size"] = self.__download_size
        return product_info

    def get_fulfilment_info(self):
        return f"This product is delivered digitally."
