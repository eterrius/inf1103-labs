# --- Imports --- #
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


# --- Classes --- #
class Inventory:
    def __init__(self):
        # self.__inventory = {}
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def display_all(self):
        if not self.products:
            print("\nInventory is empty.\n")
            return

        print("\nCurrent Inventory")
        print("-" * 50)

        for product in self.products:
            product_info = product.display_information()

            message = f"ID: {product_info['product_id']} | Name: {product_info['name']} | Price: ${str(product_info['price'])} | Stock: {product_info['stock']} | Supplier: {product_info['supplier']['name']}"

            if product_info["type"] == "physical":
                message += f" | Weight: {product_info['weight']} kg"

            elif product_info["type"] == "digital":
                message += f" | Download Size: {product_info['download_size']} MB"

            print(message)

        print("-" * 50)
        print()

    def search_product(self, product_id: str) -> Product | None:
        for product in self.products:
            product_info = product.display_information()

            if product.display_information()["product_id"] == product_id:
                print("\nProduct Found")
                print("-" * 50)
                print("ID:", product_id)
                print("Name:", product_info["name"])
                print("Price:", product_info["price"])
                print("Stock:", product_info["stock"])
                print("Supplier:", product_info["supplier"]["name"])

                if isinstance(product, PhysicalProduct):
                    print("Weight:", product_info["weight"], "kg")
                    print("Shipping Cost: $", product.calculate_shipping_cost())
                    print(product.get_fulfilment_info())

                elif isinstance(product, DigitalProduct):
                    print("Download Size:", product_info["download_size"], "MB")
                    print(product.get_fulfilment_info())

                print("-" * 50, "\n")
                return product

        print("\nProduct not found. \n")
        return None

    def keys(self):
        # return a list of product IDs in the inventory
        return [
            product.display_information()["product_id"] for product in self.products
        ]
