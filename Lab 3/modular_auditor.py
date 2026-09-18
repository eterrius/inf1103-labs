inv = 0
wrong = 0

while True:
    stock = input("Please enter stock quantity: ")

    if stock.isdigit() and int(stock) >= 0:
        if int(stock) + inv > 500:
            print("Stock quantity exceeds maximum limit.")
            break

        inv += int(stock)
    

    else:
        wrong += 1
        print("Invalid input. Please enter a non-negative integer.")

    if stock == "quit":
        print(f"Total Units Processed: {inv}")
        print(f"Number of Failed/Rejected Entries: {wrong}")
        break