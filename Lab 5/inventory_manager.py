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


def get_valid_input(input_type, user_input):
    # Menu
    if input_type == "menu":
        if user_input in ["1", "2", "3", "4", "5", "6"]:
            return user_input

        print("\nInvalid menu option. Please input again. ")
        return get_menu()

    # Product Validation
    elif input_type == "product_id":
        if user_input.upper().startswith("P") and user_input[1:].isdigit():
            return user_input.upper()

        print("\nInvalid product ID. Please input again. ")
        return get_valid_input("product_id", input("Product ID: "))

    elif input_type == "product_name":
        if user_input.strip() != "":
            return user_input.strip()

        print("\nInvalid product name. Please input again. ")
        return get_valid_input("product_name", input("Product Name: "))

    elif input_type == "product_price":
        try:
            price = float(user_input)
            if price < 0:
                raise ValueError
            return price
        except ValueError:
            print("\nInvalid product price. Please input a non-negative number.")
            return get_valid_input("product_price", input("Product Price: "))

    elif input_type == "product_stock":
        if user_input.isdigit() and int(user_input) >= 0:
            return int(user_input)

        print("\nInvalid product stock. Please input a non-negative integer.")
        return get_valid_input("product_stock", input("Product Stock: "))


def add_product(inventory):
    product = {}
    product_id = get_valid_input("product_id", input("Product ID: "))

    if product_id not in inventory.keys():
        inventory[product_id] = product
        product["name"] = get_valid_input("product_name", input("Product Name: "))
        product["price"] = get_valid_input("product_price", input("Product Price: "))
        product["stock"] = get_valid_input("product_stock", input("Product Stock: "))

        print("\nProduct added successfully!\n")

        return inventory

    print("\nProduct ID already exists. Please input again. ")
    return add_product(inventory)


def display_inventory(inventory):
    if not inventory:
        print("\nInventory is empty.\n")
        return

    print("\nCurrent Inventory")
    print("-" * 50)
    for product_id, product in inventory.items():
        print(
            f"ID: {product_id} | Name: {product['name']} | Price: ${str(product['price'])} | Stock: {product['stock']}"
        )
    print("-" * 50)
    print()

    return


def update_stock(inventory):
    product_id = get_valid_input("product_id", input("Enter Product ID: "))

    if product_id in inventory.keys():
        product = inventory[product_id]

        print(
            f"Product found: \nName: {product['name']} \nCurrent Stock: {product['stock']}"
        )

        inventory[product_id]["stock"] = get_valid_input(
            "product_stock", input("\nNew Stock Quantity: ")
        )

        print("\nStock updated successfully!\n")

    else:
        print("\nProduct not found. \n")

    return inventory


def search_product(inventory):
    search_id = get_valid_input("product_id", input("Enter Product ID: "))

    if search_id in inventory.keys():
        product = inventory[search_id]

        print("\nProduct Found")
        print("-" * 50)
        print("ID:", search_id)
        print("Name:", product["name"])
        print("Price:", product["price"])
        print("Stock:", product["stock"])
        print("-" * 50, "\n")

    else:
        print("\nProduct not found. \n")


def save_inventory(inv_name, inventory):
    with open(inv_name, "w") as file:
        file.write(json.dumps(inventory, indent=2))


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
        print("\nAdd New Product")
        inventory = add_product(inventory)

    elif choice == "3":
        print("\nUpdate Stock")
        inventory = update_stock(inventory)

    elif choice == "4":
        print("\nSearch Product")
        search_product(inventory)

    elif choice == "5":
        print("\nSaving inventory...")
        save_inventory(INV_NAME, inventory)
        print(f"Inventory saved successfully to {INV_NAME}.\n")

    elif choice == "6":
        print("\nSaving inventory before exit...")
        save_inventory(INV_NAME, inventory)
        print("Inventory saved successfully.")
        print("\nThank you for using the Inventory Management System.")
        break


print("Program terminated.")
