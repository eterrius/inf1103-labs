# --- Imports --- #
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from file_handler import FileHandler
from supplier import Supplier
from order import Order


# --- Classes --- #
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

    def display_menu(self) -> None:
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

    def get_valid_input(self, input_type: str, user_input: str) -> str | float | int:
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

    def add_product(self) -> None:
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
                    supplier=Supplier(
                        supplier_id=input("Supplier ID: "),
                        name=input("Supplier Name: "),
                        contact_email=input("Supplier Contact Email: "),
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
                    supplier=Supplier(
                        supplier_id=input("Supplier ID: "),
                        name=input("Supplier Name: "),
                        contact_email=input("Supplier Contact Email: "),
                    ),
                )

            self.__inventory.add_product(product=product)

        else:
            print("\nProduct ID already exists. Please input again. ")
            return self.add_product()

    def input_product_type(self) -> str:
        product_type = input("Enter Product Type (Physical/Digital): ").strip().lower()

        if product_type in ["physical", "digital"]:
            return product_type

        print("\nInvalid product type. Please input again. ")
        return self.input_product_type()

    def search_product(self) -> Product | None:
        product_id = self.get_valid_input("product_id", input("Enter Product ID: "))
        return self.__inventory.search_product(product_id=product_id)

    def update_stock(self) -> None:
        product = self.search_product()

        if product:
            product.update_stock(
                new_stock=self.get_valid_input(
                    "product_stock", input("\nNew Stock Quantity: ")
                )
            )

            print("\nStock updated successfully!\n")

    def get_choice(self) -> str:
        choice = input("Enter option: ")
        return choice

    def validate_choice(self, choice: str) -> bool:
        if choice in self.__options.keys():
            return True
        else:
            print("\nInvalid choice. Please try again.\n")
            return False

    def execute_choice(self, choice: str) -> None:
        if self.validate_choice(choice):
            self.__options[choice]()

    def exit_program(self) -> None:
        print("\nSaving inventory before exit...")
        self.save_inventory()
        print("\nProgram terminated.\n")
        exit()

    def get_inventory(self) -> Inventory:
        return self.__inventory

    def load_inventory(self) -> None:
        self.__handler.load_inventory()  # Load inventory from file

    def save_inventory(self) -> None:
        self.__handler.save_inventory()  # Save inventory to file

    def run(self) -> None:
        self.load_inventory()

        while True:
            self.display_menu()

            choice = self.get_choice()
            self.execute_choice(choice)


# --- Main Program --- #
if __name__ == "__main__":
    main_program = Main()
    main_program.run()
