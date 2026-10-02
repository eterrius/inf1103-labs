# --- Imports --- #


# --- Functions --- #
def get_menu():
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

    return get_valid_input("menu", input("Enter option: "))


def get_valid_input(input_type, user_input):
    # Menu
    if input_type == "menu":
        if user_input in ["1", "2", "3", "4", "5", "6"]:
            return user_input

        print("Invalid menu option. Please input again. ")
        return get_menu()

    # Add Product
    elif input_type == "product_id":
        if user_input.upper().startswith("P") and user_input[1:].isdigit():
            return user_input.upper()

        print("Invalid product ID. Please input again. ")
        return get_valid_input("product_id", input("Product ID: "))

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
    product["id"] = get_valid_input("product_id", input("Product ID: "))
    product["name"] = input("Product Name: ")
    product["price"] = get_valid_input("product_price", input("Product Price: "))
    product["stock"] = get_valid_input("product_stock", input("Product Stock: "))

    inventory[product["id"]] = product
    print("Product added successfully!")

    return inventory


# --- Constants and Variables --- #
INV_PATH = "inventory.json"
inventory = {}

# --- Main Program --- #
while True:
    print("""========================================
INVENTORY MANAGEMENT SYSTEM
========================================""")
    choice = get_menu()

    if choice == "2":
        inventory = add_product(inventory)
        print(inventory)

    elif choice == "6":
        print("Thank you for using the Inventory Management System.")
        break


print("Program terminated.")
