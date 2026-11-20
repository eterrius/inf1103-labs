# --- Imports --- #
from .digital_product import DigitalProduct
from .physical_product import PhysicalProduct
from .product import Product
from supplier import Supplier


# --- Classes --- #
class ProductFactory:
    @staticmethod
    def create(
        product_id: str,
        type: str,
        name: str,
        price: float,
        stock: int,
        weight_or_size: float,
        supplier: Supplier,
    ) -> Product:
        if type == "physical":
            product = PhysicalProduct(
                product_id, type, name, price, stock, weight_or_size, supplier
            )
        elif type == "digital":
            product = DigitalProduct(
                product_id, type, name, price, stock, weight_or_size, supplier
            )

        else:
            raise ValueError(f"Unknown product type: {type}")

        product.validate_price()
        product.validate_stock()

        return product
