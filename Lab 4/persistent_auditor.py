# --- Functions --- #
def get_valid_input(mode="stock"):
    if mode == "stock":
        result = input("Please enter stock quantity: ")

        if result.isdigit() and int(result) >= 0:
            return int(result)

        elif result == "quit":
            return result

        else:
            print("Invalid input. Please enter a non-negative integer.")
            return None

    elif mode == "product":
        result = input("Please enter product name: ")

        if result == "":
            print("Invalid input. Please enter something. ")
            return None

        return result


def process_delivery(product, new_value):
    product[2] += new_value
    print(f"\nProduct processed: \n{product}\n")
    return product


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def load_inventory(inv_path):
    result = []

    try:
        with open(inv_path, "r") as file:
            for line in file.readlines():
                current = line.strip().split(", ")
                current[0], current[2] = int(current[0]), int(current[2])

                result.append(current)

            return result

    except FileNotFoundError:
        return result


def save_inventory(inv, inv_path):
    with open(inv_path, "w") as file:
        for line in inv:
            file.write(f"{', '.join(map(str, line))}\n")

    return


def get_product(inventory):
    product = get_valid_input("product")

    if product is None:
        return None

    elif product == "quit":
        return product

    for line in inventory:
        if product in line:
            return line

    new_product = [inventory[-1][0] + 1, product, 0]
    inventory.append(new_product)

    return new_product


# --- Constants --- #
INV_PATH = "inventory.txt"


# --- Variables --- #
wrong = 0
inv = load_inventory(INV_PATH)

# --- Main Program --- #
while True:
    product = get_product(inv)

    if product != "quit":
        if product is None:
            wrong += 1
            continue

        stock = get_valid_input()

        if stock is None:
            wrong += 1

        elif stock != "quit":
            if stock + product[2] > 500:
                print("Stock quantity exceeds maximum limit.")
                break

            product = process_delivery(product, stock)
            cost = stock * 10  # Assuming delivery per unit costs $10
            tax = calculate_tax(cost)

        else:
            save_inventory(inv, INV_PATH)
            break

    else:
        save_inventory(inv, INV_PATH)
        break

generate_report(inv, wrong)
