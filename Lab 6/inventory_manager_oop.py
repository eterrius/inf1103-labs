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


class Inventory:
    def __init__(self):
        self.__inventory = {}

    def add_product(self, product):
        self.__inventory[product.get_product_info()["product_id"]] = product

    def display_all(self):
        if not self.__inventory:
            print("\nInventory is empty.\n")
            return

        print("\nCurrent Inventory")
        print("-" * 50)
        for product_id, product in self.__inventory.items():
            product_info = product.get_product_info()
            print(
                f"ID: {product_id} | Name: {product_info['name']} | Price: ${str(product_info['price'])} | Stock: {product_info['stock']}"
            )

        print("-" * 50)
        print()

    def update_stock(self, product_id, new_stock):
        if product_id in self.__inventory.keys():
            self.__inventory[product_id].update_stock(new_stock)
            print("\nStock updated successfully!\n")
        else:
            print("\nProduct not found. \n")

    def search_product(self, product_id):
        if product_id in self.__inventory.keys():
            product = self.__inventory[product_id].get_product_info()

            print("\nProduct Found")
            print("-" * 50)
            print("ID:", product_id)
            print("Name:", product["name"])
            print("Price:", product["price"])
            print("Stock:", product["stock"])
            print("-" * 50, "\n")

        else:
            print("\nProduct not found. \n")


# --- Functions --- #

# --- Main Program --- #
if __name__ == "__main__":
    inventory = Inventory()  # creating the inventory object from the Inventory class

    product1 = Product(
        "P001", "Laptop", 1200.00, 15
    )  # creating product from Product class, via init
    product2 = Product("P002", "Mouse", 25.50, 40)

    inventory.add_product(
        product1
    )  # pass the product to inventory class to store in a list
    inventory.add_product(product2)

    inventory.display_all()  # display the inventory
    inventory.update_stock("P001", 20)  # update stock for product with ID "P001"
    inventory.search_product("P001")  # search for product with ID "P002"
    inventory.display_all()  # display all products in the inventory
