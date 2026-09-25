# --- Functions --- #
def get_valid_input(valid):
    result = input("Please enter stock quantity: ")

    if result.isdigit() and int(result) >= 0:
        valid += result
        return int(result), valid

    elif result == "quit":
        return result, valid

    else:
        print("Invalid input. Please enter a non-negative integer.")
        return None, valid


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def read_inventory_from_file(filename):
    try:
        with open(filename, "r") as file:
            try:
                return int(file.read().strip())

            except ValueError:
                return 0

    except FileNotFoundError:
        return 0


def save_inventory(inv, success, inv_path):
    with open("inventory.txt", "w") as file:
        file.write(f"{inv}\n{success}")

    return


# --- Constants --- #
INV_PATH = "inventory.txt"


# --- Variables --- #
wrong = 0
inv = read_inventory_from_file(INV_PATH)
success = []

# --- Main Program --- #
while True:
    stock, success = get_valid_input(success)

    if stock is None:
        wrong += 1

    elif stock != "quit":
        if stock + inv > 500:
            print("Stock quantity exceeds maximum limit.")
            break

        inv = process_delivery(inv, stock)
        cost = stock * 10  # Assuming delivery per unit costs $10
        tax = calculate_tax(cost)

    else:
        save_inventory(inv, success, INV_PATH)
        break

generate_report(inv, wrong)
