inv = 0


while True:
    stock = input("Please enter stock quantity: ")

    if stock.isdigit() and int(stock) >= 0:
        if int(stock) + inv > 500:
            print("Stock quantity exceeds maximum limit.")
            break

        inv += int(stock)
    

    else:
        print("Invalid input. Please enter a non-negative integer.")

    if stock == "quit":
        break