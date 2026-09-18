inv = 0
wrong = 0

def get_valid_input():
    result = input("Please enter stock quantity: ")

    if result.isdigit() and int(result) >= 0:
        return int(result)
    
    elif result == "quit":
        return result

    else:
        print("Invalid input. Please enter a non-negative integer.")
        return None

while True:
    stock = get_valid_input()

    if stock is None:
        wrong += 1

    elif stock != "quit":
        if int(stock) + inv > 500:
            print("Stock quantity exceeds maximum limit.")
            break

        inv += int(stock)


    else:

        print(f"Total Units Processed: {inv}")
        print(f"Number of Failed/Rejected Entries: {wrong}")
        break