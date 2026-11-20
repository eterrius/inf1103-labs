# --- Imports --- #
import csv
from .file_handler import FileHandler
from inventory import Inventory
from products import ProductFactory
from supplier import Supplier


# --- Classes --- #
class CSVFileHandler(FileHandler):
    def __init__(self, inventory: Inventory, filename: str = "inventory.csv"):
        super().__init__(inventory, filename)
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
                        "product_type",
                        "product_id",
                        "name",
                        "price",
                        "stock_quantity",
                    ],
                )
                next(reader)  # Skip the header row
                for row in reader:
                    try:
                        product_id = row["product_id"]
                        product_type = row["product_type"]
                        product_name = row["name"]
                        product_price = float(row["price"])
                        product_stock = int(row["stock_quantity"])

                        product_weight_or_size = 0.0  # Default value if type is unknown
                        supplier = Supplier(
                            supplier_id=row.get("supplier_id", ""),
                            name=row.get("supplier_name", ""),
                            contact_email=row.get("supplier_contact_email", ""),
                        )

                        self._inventory.add_product(
                            ProductFactory.create(
                                product_id,
                                product_type,
                                product_name,
                                product_price,
                                product_stock,
                                product_weight_or_size,
                                supplier,
                            )
                        )

                        loaded += 1

                    except ValueError as e:
                        print(f"Error loading product {product_id}: {e}")

            print(f"{loaded} products loaded from {self.__filename}.")

        finally:
            print("Load attempt finished.")

    def save_inventory(self) -> None:
        try:
            file = open(self.__filename, mode="w", newline="")

        except Exception as e:
            print(f"Error opening file {self.__filename} for writing: {e}")

        else:
            with file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "product_id",
                        "product_type",
                        "name",
                        "price",
                        "stock_quantity",
                    ],
                )
                writer.writeheader()
                for product in self._inventory.get_all_products():
                    product_info = product.get_product_info()
                    writer.writerow(
                        {
                            "product_id": product_info["product_id"],
                            "product_type": product_info["type"],
                            "name": product_info["name"],
                            "price": product_info["price"],
                            "stock_quantity": product_info["stock"],
                        }
                    )

            print(f"Inventory saved to {self.__filename}.")

        finally:
            print("Save attempt finished.")
