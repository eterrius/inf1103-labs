import ast
import inspect
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from discount.discount_strategy import DiscountStrategy
from discount.no_discount import NoDiscount
from discount.percentage_discount import PercentageDiscount
from file_handlers import CSVFileHandler
from order import Order
from order_line import OrderLine
from products.digital_product import DigitalProduct
from products.physical_product import PhysicalProduct
from products.product_factory import ProductFactory
from supplier import Supplier

from inventory import Inventory


class TestSystemConfirmations(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "Acme Corp", "acme@example.com")
        self.product_weight = 2.5  # kg for physical products
        self.product_size = 500.0  # MB for digital products
        self.laptop = ProductFactory.create(
            "P001", "physical", "Laptop", 1000.0, 10, self.product_weight, self.supplier
        )

    # ------------------------------------------------------------------
    # 1. Order calculates totals through a DiscountStrategy & has no
    #    discount if/elif logic
    # ------------------------------------------------------------------
    def test_01_order_uses_strategy_without_discount_conditionals(self):
        order = Order("O001", NoDiscount())
        order.add_order_line(self.laptop, 2)
        self.assertAlmostEqual(order.calculate_total(), 2000.0)

        # Inspect Order source AST to confirm there are no if/elif checks on discount types
        source = inspect.getsource(Order)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                condition_src = ast.unparse(node.test).lower()
                self.assertNotIn(
                    "discount",
                    condition_src,
                    f"Order should delegate to DiscountStrategy, not branch on: {condition_src}",
                )

    # ------------------------------------------------------------------
    # 2. A new discount strategy can be added without changing Order
    # ------------------------------------------------------------------
    def test_02_new_discount_strategy_works_without_modifying_order(self):
        class FlatFiftyDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return max(0.0, total - 50.0)

        order = Order("O002", FlatFiftyDiscount())
        order.add_order_line(self.laptop, 1)
        self.assertAlmostEqual(order.calculate_total(), 950.0)

    # ------------------------------------------------------------------
    # 3. The strategy on an existing order can be changed with set_discount()
    # ------------------------------------------------------------------
    def test_03_change_strategy_with_set_discount(self):
        order = Order("O003", NoDiscount())
        order.add_order_line(self.laptop, 1)
        self.assertAlmostEqual(order.calculate_total(), 1000.0)

        order.set_discount(PercentageDiscount(0.1))  # 10% off
        self.assertAlmostEqual(order.calculate_total(), 900.0)

    # ------------------------------------------------------------------
    # 4. Products are created through ProductFactory rather than directly
    # ------------------------------------------------------------------
    def test_04_products_created_via_factory_not_directly(self):
        p_phys = ProductFactory.create(
            "P010", "physical", "Desk", 250.0, 5, self.product_weight, self.supplier
        )
        p_dig = ProductFactory.create(
            "P011", "digital", "E-Book", 20.0, 100, self.product_size, self.supplier
        )
        self.assertIsInstance(p_phys, PhysicalProduct)
        self.assertIsInstance(p_dig, DigitalProduct)

        # Verify application modules do not directly instantiate PhysicalProduct/DigitalProduct
        app_files = [
            "inventory.py",
            "inventory_manager_oop.py",
            "file_handler/csv_file_handler.py",
            "file_handler/json_file_handler.py",
        ]
        for filepath in app_files:
            if not Path(filepath).exists():
                continue
            tree = ast.parse(Path(filepath).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(
                        node.func.id,
                        {"PhysicalProduct", "DigitalProduct"},
                        f"Direct instantiation of {node.func.id} found in {filepath}",
                    )

    # ------------------------------------------------------------------
    # 5. An unknown product type raises a ValueError with a clear message
    # ------------------------------------------------------------------
    def test_05_unknown_product_type_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create(
                "P999", "service", "Consulting", 150.0, 1, 0, self.supplier
            )
        self.assertIn("service", str(ctx.exception).lower())

    # ------------------------------------------------------------------
    # 6. Invalid prices, stock quantities, and order quantities are rejected
    # ------------------------------------------------------------------
    def test_06_invalid_prices_stock_and_order_quantities_rejected(self):
        # Negative / zero price
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "P002",
                "physical",
                "Bad Price",
                -10.0,
                5,
                self.product_weight,
                self.supplier,
            )

        # Negative stock quantity
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "P003",
                "physical",
                "Bad Stock",
                10.0,
                -3,
                self.product_weight,
                self.supplier,
            )

        # Invalid order line quantities (<= 0 or exceeding available stock)
        with self.assertRaises(ValueError):
            OrderLine(self.laptop, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.laptop, -2)
        with self.assertRaises(ValueError):
            OrderLine(self.laptop, 999)

    # ------------------------------------------------------------------
    # 7. Invalid user input is handled without crashing & user is re-prompted
    # ------------------------------------------------------------------
    def test_07_invalid_user_input_reprompts_without_crashing(self):
        import inventory_manager_oop

        # Simulate entering invalid menu options/numbers before choosing exit (e.g., "0")
        simulated_inputs = ["not_a_number", "-99", "0"]
        with patch("builtins.input", side_effect=simulated_inputs) as mock_input, patch(
            "builtins.print"
        ):
            try:
                main = inventory_manager_oop.Main(CSVFileHandler, "products.csv")
                if hasattr(main, "run"):
                    main.run()
            except StopIteration:
                # Reached end of simulated inputs without crashing on invalid entries
                pass
            self.assertGreaterEqual(mock_input.call_count, 2)

    # ------------------------------------------------------------------
    # 8. A missing products file is handled gracefully
    # ------------------------------------------------------------------
    def test_08_missing_products_file_handled_gracefully(self):
        handler = CSVFileHandler(
            inventory=Inventory(), filename="non_existent_products_file_12345.csv"
        )
        missing_path = "non_existent_products_file_12345.csv"
        with patch("builtins.print"):
            # Should not raise an unhandled FileNotFoundError
            result = handler.load_inventory()
            self.assertIn(result, ([], None, {}))

    # ------------------------------------------------------------------
    # 9. Bad rows in the products file are reported and skipped; valid rows load
    # ------------------------------------------------------------------
    def test_09_bad_rows_reported_and_skipped_while_valid_rows_load(self):
        csv_content = (
            "product_type,product_id,name,price,stock_quantity,supplier_id,supplier_name,supplier_email\n"
            "physical,P100,Keyboard,50.0,10,S1,Logi,sales@logi.com\n"
            "physical,P101,BrokenPrice,not_a_float,10,S1,Logi,sales@logi.com\n"
            "unknown_type,P102,Mystery,25.0,5,S1,Logi,sales@logi.com\n"
            "digital,P103,Antivirus,30.0,50,S1,Logi,sales@logi.com\n"
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            handler = CSVFileHandler(inventory=Inventory(), filename=tmp_path)
            with patch("builtins.print") as mock_print:
                handler.load_inventory()
                products = handler._inventory.products

            # Only the 2 valid rows (P100 and P103) should load
            self.assertEqual(len(products), 2)
            # Bad rows should have been reported via print()
            self.assertTrue(mock_print.called)
        finally:
            os.remove(tmp_path)

    # ------------------------------------------------------------------
    # 10. Each except catches a specific exception (no bare except or
    #     generic Exception)
    # ------------------------------------------------------------------
    def test_10_all_except_blocks_catch_specific_exceptions(self):
        project_py_files = [
            p for p in Path(".").rglob("*.py") if p.name != Path(__file__).name
        ]
        for py_file in project_py_files:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    self.assertIsNotNone(
                        node.type,
                        f"Bare 'except:' found in {py_file}:{node.lineno}",
                    )
                    if isinstance(node.type, ast.Name):
                        self.assertNotIn(
                            node.type.id,
                            {"Exception", "BaseException"},
                            f"Overly broad 'except {node.type.id}:' in {py_file}:{node.lineno}",
                        )


if __name__ == "__main__":
    unittest.main()
