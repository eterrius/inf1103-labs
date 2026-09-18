# --- Variables --- #
inv = 0
wrong = 0


# --- Functions --- #
def get_valid_input():
    result = input("Please enter stock quantity: ")

    if result.isdigit() and int(result) >= 0:
        return int(result)

    elif result == "quit":
        return result

    else:
        print("Invalid input. Please enter a non-negative integer.")
        return None


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


# --- Main Program --- #
while True:
    stock = get_valid_input()

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
        print(f"Total Units Processed: {inv}")
        print(f"Number of Failed/Rejected Entries: {wrong}")
        break
