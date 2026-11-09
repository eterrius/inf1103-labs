# --- Classes --- #
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
            product = self.__inventory[product_id].display_information()

            print("\nProduct Found")
            print("-" * 50)
            print("ID:", product_id)
            print("Name:", product["name"])
            print("Price:", product["price"])
            print("Stock:", product["stock"])

            if product["type"] == "physical":
                print("Weight:", product["weight"], "kg")
                print(
                    "Shipping Cost: $",
                    self.__inventory[product_id].calculate_shipping_cost(),
                )
                print(
                    self.__inventory[product_id].get_fulfilment_info(),
                )

            elif product["type"] == "digital":
                print("Download Size:", product["download_size"], "MB")
                print(
                    self.__inventory[product_id].get_fulfilment_info(),
                )

            print("-" * 50, "\n")

        else:
            print("\nProduct not found. \n")
            return product_id, None

        return product_id, product

    def items(self):
        return self.__inventory.items()

    def keys(self):
        return self.__inventory.keys()
