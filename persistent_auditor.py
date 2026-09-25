import os

failedEntries = int(0)

def loadInventory():
    inventoryFileName = "inventory.txt"

    if not os.path.exists(inventoryFileName):
        return 0, []

    try:
        with open (inventoryFileName, 'r') as file:
            entries = [line.strip() for line in file.readlines() if line.strip()]

        if not entries: 
            return 0, []

        inventoryTotal = int(entries[0])

        history = [int(line) for line in entries[1:]]

        print(f"Existing Invetory: {inventoryTotal} units with {len(history)} entries")
        return inventoryTotal, history

    except(ValueError, IOError):
        print("Warning: There is no inventory.txt, creating a new file")
        return 0, []


def saveInventory(total_units, history):
    with open("inventory.txt", "w") as file:
        file.write(f"Total Stock: {total_units}\n")
        for item in history:
            file.write(f"Stock entry: {item}\n")

    print("Data saved to inventory.txt")


    

def getValidInput():
    global failedEntries

    while True:
        userInput = input("Enter stock value (or 'quit'): ")

        if userInput.lower() == "quit":
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

inventory, transactionHistory = loadInventory()

while True:
    value = getValidInput()

    if value == 'quit':
        break

    tax = calculateTax(value)
    print("Tax amount: " + str(tax))

    transactionHistory.append(value)
    

    inventory = processDelivery(inventory, value)

    if inventory > 500:
        print("Stock currently exceeds 500")
        break
    else:
        print("Stock amount: " + str(inventory))

saveInventory(inventory, transactionHistory)

generateReport(inventory, failedEntries)