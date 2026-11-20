# --- Imports --- #
import csv
from .file_handler import FileHandler
from inventory import Inventory
from products import ProductFactory


# --- Classes --- #
class CSVFileHandler(FileHandler):
    def __init__(self, inventory: Inventory, filename: str = "inventory.csv"):
        super().__init__(inventory)
        self.__filename = filename

    def load_inventory(self) -> dict:
        try:
            file = open(self.__filename, mode="r", newline="")

        except FileNotFoundError:
            print(f"{self.__filename} not found.")

        else:
            with file:
                loaded = 0
                reader = csv.DictReader(
                    file,
                    fieldnames=[
                        "product_id",
                        "product_type",
                        "name",
                        "price",
                        "stock_quantity",
                    ],
                )
                for row in reader:
                    product_id = row["product_id"]
                    product_type = row["product_type"]
                    product_name = row["name"]
                    product_price = float(row["price"])
                    product_stock = int(row["stock_quantity"])

                    # if product_type == "physical":
                    #     product_weight_or_size = float(row.get("weight", 0))
                    # elif product_type == "digital":
                    #     product_weight_or_size = float(row.get("download_size", 0))

                    try:
                        self._inventory.add_product(
                            ProductFactory.create(
                                product_id,
                                product_type,
                                product_name,
                                product_price,
                                product_stock,
                                # product_weight_or_size,
                            )
                        )
                        loaded += 1

                    except ValueError as e:
                        print(f"Error loading product {product_id}: {e}")

            print(f"{loaded} products loaded from {self.__filename}.")

        finally:
            print("Load attempt finished.")
