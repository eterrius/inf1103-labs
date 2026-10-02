# --- Imports --- #
import json


# --- Functions --- #
def load_inventory(inv_name):
    print()

    try:
        with open(inv_name, "r") as file:
            print(f"{inv_name} found.")
            inventory = json.load(file)
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


def get_menu():
    return get_valid_input("menu", input("Enter option: "))


def get_valid_input(input_type, user_input, inventory={}):
    # Menu
    if input_type == "menu":
        if user_input in ["1", "2", "3", "4", "5", "6"]:
            return user_input

        print("Invalid menu option. Please input again. ")
        return get_menu()

    # Add Product
    elif input_type == "product_id":
        if user_input.upper().startswith("P") and user_input[1:].isdigit():
            if user_input.upper() not in inventory.keys():
                return user_input.upper()

            print("Product ID already exists. Please input again. ")
            return get_valid_input("product_id", input("Product ID: "), inventory)

        print("Invalid product ID. Please input again. ")
        return get_valid_input("product_id", input("Product ID: "), inventory)

    elif input_type == "product_name":
        if user_input.strip() != "":
            return user_input.strip()

        print("Invalid product name. Please input again. ")
        return get_valid_input("product_name", input("Product Name: "))

    elif input_type == "product_price":
        try:
            price = float(user_input)
            if price < 0:
                raise ValueError
            return price
        except ValueError:
            print("Invalid product price. Please input a non-negative number.")
            return get_valid_input("product_price", input("Product Price: "))

    elif input_type == "product_stock":
        if user_input.isdigit() and int(user_input) >= 0:
            return int(user_input)

        print("Invalid product stock. Please input a non-negative integer.")
        return get_valid_input("product_stock", input("Product Stock: "))


def add_product(inventory):
    print("Add New Product")

    product = {}
    id = get_valid_input("product_id", input("Product ID: "), inventory)
    product["name"] = get_valid_input("product_name", input("Product Name: "))
    product["price"] = get_valid_input("product_price", input("Product Price: "))
    product["stock"] = get_valid_input("product_stock", input("Product Stock: "))

    inventory[id] = product
    print("Product added successfully!")

    return inventory


def display_inventory(inventory):
    if not inventory:
        print("\nInventory is empty.\n")
        return

    print("\nCurrent Inventory")
    print("-" * 50)
    for product_id, product in inventory.items():
        print(
            f"ID: {product_id} | Name: {product['name']} | Price: {"$" + str(product['price'])} | Stock: {product['stock']}"
        )
    print("-" * 50)
    print()

    return


# --- Constants --- #
INV_NAME = "inventory.json"


# --- Main Program --- #
print("""========================================
INVENTORY MANAGEMENT SYSTEM
========================================""")

inventory = load_inventory(INV_NAME)

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

while True:

    choice = get_menu()

    if choice == "1":
        display_inventory(inventory)

    elif choice == "2":
        inventory = add_product(inventory)
        print(inventory)

    elif choice == "6":
        print("\nThank you for using the Inventory Management System.")
        break


print("Program terminated.")
