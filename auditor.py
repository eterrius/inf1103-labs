inv = 0


while True:
    stock = input("Please enter stock quantity: ")

    if stock.isdigit():
        stock = int(stock)

    else:
        print("Invalid input. Please enter a non-negative integer.")

    if stock == "quit":
        break