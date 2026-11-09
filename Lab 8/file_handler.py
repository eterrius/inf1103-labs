# --- Imports --- #
import json
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


# --- Classes --- #
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
                supplier_data = product_data.get("supplier", {})
                supplier = Supplier(
                    supplier_data.get("supplier_id", ""),
                    supplier_data.get("name", ""),
                    supplier_data.get("contact_email", ""),
                )

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
                        supplier,
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
                        supplier,
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
        for product in self._inventory.products:
            product_info = product.display_information()
            product_id = product_info["product_id"]

            inventory_data[product_id] = {
                "type": product_info["type"],
                "name": product_info["name"],
                "price": product_info["price"],
                "stock": product_info["stock"],
                "supplier": product_info["supplier"],
            }

            if product_info["type"] == "physical":
                inventory_data[product_id]["weight"] = product_info.get("weight", 0)
            elif product_info["type"] == "digital":
                inventory_data[product_id]["download_size"] = product_info.get(
                    "download_size", 0
                )

        return inventory_data
