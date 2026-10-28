# --- Imports --- #
import json


# --- Classes --- #
class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def get_product_info(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

# --- Functions --- #

# --- Main Program --- #
if __name__ == "__main__":
    product1 = Product("P001", "Laptop", 1200.00, 15) # creating product from Product class, via init
    product2 = Product("P002", "Mouse", 25.50, 40)

    print(product1) # calling get_product_info method to get product info
    print(product2)
