inventory = int(0)
failedEntries = int(0)

while True:
    userInput = input("Enter stock value (or 'quit'): ")

    if userInput.lower() == "quit":
        break
    if not userInput.isdigit():
          if userInput.startswith("-"):
                failedEntries += 1
                print("Negative numbers are not allowed. Please enter a positive number")
          else:
                print("Characters are not allowed. Please enter a number")
                failedEntries += 1
    
    if userInput.isdigit():
            inventory = inventory + int(userInput)
            if inventory > 500:
                   print("Stock currently exceeds 500")
                   break
            else:
                   print("Stock: " + str(inventory))

print("Stock: " + str(inventory))
print("Failed entries: " +str(failedEntries))

        
            
        
    
