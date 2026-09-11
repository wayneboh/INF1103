inventory = 0

while True:
    userInput = input("Enter stock value (or 'quit'): ")

    if userInput.lower() == "quit":
        break

    if userInput.isdigit():
        print("Works")
    
