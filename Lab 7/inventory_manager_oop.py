# --- Imports --- #
import json
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


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, type, name, price, stock, weight):
        super().__init__(product_id, type, name, price, stock)
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


class Inventory:
    def __init__(self):
        self.__inventory = {}

    def add_product(self, product):
        self.__inventory[product.display_information()["product_id"]] = product

    def display_all(self):
        if not self.__inventory:
            print("\nInventory is empty.\n")
            return

        print("\nCurrent Inventory")
        print("-" * 50)
        for product_id, product in self.__inventory.items():
            product_info = product.display_information()

            message = f"ID: {product_id} | Name: {product_info['name']} | Price: ${str(product_info['price'])} | Stock: {product_info['stock']}"

            if product_info["type"] == "physical":
                message += f" | Weight: {product_info['weight']} kg"

            elif product_info["type"] == "digital":
                message += f" | Download Size: {product_info['download_size']} MB"

            print(message)

        print("-" * 50)
        print()

    def update_stock(self, product_id, new_stock):
        self.__inventory[product_id].update_stock(new_stock)
        print("\nStock updated successfully!\n")

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
            return product_id, None

        return product_id, product

    def items(self):
        return self.__inventory.items()

    def keys(self):
        return self.__inventory.keys()


class Main:
    def __init__(self):
        self.__inventory = Inventory()
        self.__handler = FileHandler(self.__inventory)

        self.__options = {
            "1": self.__inventory.display_all,
            "2": self.add_product,
            "3": self.update_stock,
            "4": self.search_product,
            "5": self.save_inventory,
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

    def get_valid_input(self, input_type, user_input):
        # Product Validation
        if input_type == "product_id":
            if user_input.upper().startswith("P") and user_input[1:].isdigit():
                return user_input.upper()

            print("\nInvalid product ID. Please input again. ")
            return self.get_valid_input("product_id", input("Product ID: "))

        elif input_type == "product_name":
            if user_input.strip() != "":
                return user_input.strip()

            print("\nInvalid product name. Please input again. ")
            return self.get_valid_input("product_name", input("Product Name: "))

        elif input_type == "product_price":
            try:
                price = float(user_input)
                if price < 0:
                    raise ValueError
                return price
            except ValueError:
                print("\nInvalid product price. Please input a non-negative number.")
                return self.get_valid_input("product_price", input("Product Price: "))

        elif input_type == "product_stock":
            if user_input.isdigit() and int(user_input) >= 0:
                return int(user_input)

            print("\nInvalid product stock. Please input a non-negative integer.")
            return self.get_valid_input("product_stock", input("Product Stock: "))

        elif input_type == "product_weight":
            try:
                weight = float(user_input)
                if weight < 0:
                    raise ValueError
                return weight
            except ValueError:
                print("\nInvalid product weight. Please input a non-negative number.")
                return self.get_valid_input(
                    "product_weight", input("Product Weight (kg): ")
                )

        elif input_type == "product_download_size":
            try:
                download_size = float(user_input)
                if download_size < 0:
                    raise ValueError
                return download_size
            except ValueError:
                print(
                    "\nInvalid product download size. Please input a non-negative number."
                )
                return self.get_valid_input(
                    "product_download_size", input("Product Download Size (MB): ")
                )

    def add_product(self):
        product_id = self.get_valid_input("product_id", input("Enter Product ID: "))

        if product_id not in self.__inventory.keys():
            product_type = self.input_product_type()

            if product_type == "physical":
                product = PhysicalProduct(
                    product_id=product_id,
                    type="physical",
                    name=self.get_valid_input("product_name", input("Product Name: ")),
                    price=self.get_valid_input(
                        "product_price", input("Product Price: ")
                    ),
                    stock=self.get_valid_input(
                        "product_stock", input("Product Stock: ")
                    ),
                    weight=self.get_valid_input(
                        "product_weight", input("Product Weight (kg): ")
                    ),
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    product_id=product_id,
                    type="digital",
                    name=self.get_valid_input("product_name", input("Product Name: ")),
                    price=self.get_valid_input(
                        "product_price", input("Product Price: ")
                    ),
                    stock=self.get_valid_input(
                        "product_stock", input("Product Stock: ")
                    ),
                    download_size=self.get_valid_input(
                        "product_download_size", input("Product Download Size (MB): ")
                    ),
                )

            self.__inventory.add_product(product=product)

        else:
            print("\nProduct ID already exists. Please input again. ")
            return self.add_product()

    def input_product_type(self):
        product_type = input("Enter Product Type (Physical/Digital): ").strip().lower()

        if product_type in ["physical", "digital"]:
            return product_type

        print("\nInvalid product type. Please input again. ")
        return self.input_product_type()

    def search_product(self):
        product_id = self.get_valid_input("product_id", input("Enter Product ID: "))
        return self.__inventory.search_product(product_id=product_id)

    def update_stock(self):
        product_id, product = self.search_product()

        if product:
            self.__inventory.update_stock(
                product_id=product_id,
                new_stock=self.get_valid_input(
                    "product_stock", input("\nNew Stock Quantity: ")
                ),
            )

    def get_choice(self):
        choice = input("Enter option: ")
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
        print("\nSaving inventory before exit...")
        self.save_inventory()
        print("\nProgram terminated.\n")
        exit()

    def get_inventory(self):
        return self.__inventory

    def load_inventory(self):
        self.__handler.load_inventory()  # Load inventory from file

    def save_inventory(self):
        self.__handler.save_inventory()  # Save inventory to file

    def run(self):
        self.load_inventory()

        while True:
            self.display_menu()

            choice = self.get_choice()
            self.execute_choice(choice)


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
                if product_data["type"] == "physical":
                    product = PhysicalProduct(
                        product_id,
                        product_data["type"],
                        product_data["name"],
                        product_data["price"],
                        product_data["stock"],
                        product_data.get(
                            "weight", 0
                        ),  # Default weight to 0 if not present
                    )

                elif product_data["type"] == "digital":
                    product = DigitalProduct(
                        product_id,
                        product_data["type"],
                        product_data["name"],
                        product_data["price"],
                        product_data["stock"],
                        product_data.get(
                            "download_size", 0
                        ),  # Default download size to 0 if not present
                    )

                self._inventory.add_product(product)

            print("Inventory loaded successfully.")
            return inventory

        except FileNotFoundError:
            print("Inventory file not found. Starting with an empty inventory.")
            return {}

        except (json.JSONDecodeError, KeyError):
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
            product_info = product.display_information()
            inventory_data[product_id] = {
                "type": product_info["type"],
                "name": product_info["name"],
                "price": product_info["price"],
                "stock": product_info["stock"],
            }

            if product_info["type"] == "physical":
                inventory_data[product_id]["weight"] = product_info.get("weight", 0)
            elif product_info["type"] == "digital":
                inventory_data[product_id]["download_size"] = product_info.get(
                    "download_size", 0
                )

        return inventory_data


# --- Functions --- #

# --- Main Program --- #
if __name__ == "__main__":
    main_program = Main()
    main_program.run()
