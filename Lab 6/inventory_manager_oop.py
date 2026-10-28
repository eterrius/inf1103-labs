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

    def items(self):
        return self.__inventory.items()


class Main:
    def __init__(self):
        self.__inventory = Inventory()
        self.__handler = FileHandler(self.__inventory)

        self.__options = {
            "1": self.__inventory.display_all,
            "2": self.__inventory.add_product,
            "3": self.__inventory.update_stock,
            "4": self.__inventory.search_product,
            "5": self.save_inventory,  # This option is a placeholder for saving the inventory
            "6": self.exit_program,
        }

    def display_menu(self):
        print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
""")
        print()

    def get_choice(self):
        choice = input("Enter your choice (1-6): ")
        return choice

    def validate_choice(self, choice):
        if choice in self.__options.keys():
            return True
        else:
            print("\nInvalid choice. Please try again.\n")
            return False

    def execute_choice(self, choice):
        if self.validate_choice(choice):
            self.__options[choice]()

    def exit_program(self):
        print("\nProgram terminated.\n")
        exit()

    def get_inventory(self):
        return self.__inventory

    def load_inventory(self):
        self.__handler.load_inventory()  # Load inventory from file

    def save_inventory(self):
        self.__handler.save_inventory()  # Save inventory to file


class FileHandler:
    def __init__(self, inventory, filename="inventory.json"):
        self.__filename = filename
        self._inventory = inventory

    def load_inventory(self):
        inv_name = self.__filename

        try:
            with open(inv_name, "r") as file:
                print(f"{inv_name} found.")
                inventory = json.load(file)

            for product_id, product_data in inventory.items():
                product = Product(
                    product_id,
                    product_data["name"],
                    product_data["price"],
                    product_data["stock"],
                )

                self._inventory.add_product(product)

            print("Inventory loaded successfully.")
            return inventory

        except FileNotFoundError:
            print("Inventory file not found. Starting with an empty inventory.")
            return {}

        except json.JSONDecodeError:
            print(
                "Error decoding JSON, file may be empty or corrupted. Starting with an empty inventory."
            )
            return {}

    def save_inventory(self):
        inv_name = self.__filename
        inventory_data = self.parse_inventory()

        try:
            with open(inv_name, "w") as file:
                file.write(json.dumps(inventory_data, indent=2))
                print("Inventory saved successfully.")

        except Exception as e:
            print(f"Error saving inventory: {e}")

    def parse_inventory(self):
        inventory_data = {}
        for product_id, product in self._inventory.items():
            product_info = product.get_product_info()
            inventory_data[product_id] = {
                "name": product_info["name"],
                "price": product_info["price"],
                "stock": product_info["stock"],
            }
        return inventory_data


# --- Functions --- #

# --- Main Program --- #
if __name__ == "__main__":
    main_program = Main()

    main_program.load_inventory()  # Load inventory from file at the start

    main_program.display_menu()
    inventory = (
        main_program.get_inventory()
    )  # creating the inventory object from the Inventory class

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

    main_program.get_inventory().display_all()  # display the main program's inventory again

    main_program.save_inventory()  # Save inventory to file at the end
