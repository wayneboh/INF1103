failedEntries = int(0)

def getValidInput():
    global failedEntries

    while True:
        userInput = input("Enter stock value (or 'quit'): ")

        if userInput == "quit":
            return "quit"

        if not userInput.isdigit():
          failedEntries += 1
          if userInput.startswith("-"):
                print("Negative numbers are not allowed. Please enter a positive number")
          else:
                print("Characters and spaces are not allowed. Please enter a number")
          continue
        return int(userInput)

          
def processDelivery(currentInventory, newInventory):
    return currentInventory + newInventory

def calculateTax(valueAmount):
    return int(valueAmount) * 0.10

def generateReport(totalUnits, failedAttemptsCount):
    print("Total Units: " + str(totalUnits))
    print("Failed Entries: " + str(failedAttemptsCount))

inventory = int(0)

while True:
    value = getValidInput()

    if value == 'quit':
        break

    tax = calculateTax(value)
    print("Tax amount: " + str(tax))

    inventory = processDelivery(inventory, value)

    if inventory > 500:
        print("Stock currently exceeds 500")
        break
    else:
        print("Stock amount: " + str(inventory))

generateReport(inventory, failedEntries)
                




        
            
        
    
