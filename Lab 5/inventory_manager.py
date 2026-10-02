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
    if input_type == "menu":
        if user_input in ["1", "2", "3", "4", "5", "6"]:
            return user_input

        print("Invalid menu option. Please input again. ")
        return get_menu()


# --- Constants --- #
INV_PATH = "inventory.json"


# --- Main Program --- #
print("""========================================
INVENTORY MANAGEMENT SYSTEM
========================================""")
get_menu()