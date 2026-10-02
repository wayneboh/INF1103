import json
import os

inventoryFileName = "inventory.json"


def saveInventory(inventory):
    with open(inventoryFileName, "w") as file:
        json.dump(inventory, file, indent=4)


def loadInventory():
    if not os.path.exists(inventoryFileName):
        print("No inventory.json found, starting a new inventory.")
        inventory = {}
        saveInventory(inventory)
        return inventory

    print("inventory.json found.")
    try:
        with open(inventoryFileName, "r") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
        return inventory
    except (ValueError, IOError):
        print("Could not read inventory.json, starting with an empty inventory.")
        return {}

def getNonEmptyInput(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def getValidNumber(prompt, wholeOnly=False):
    while True:
        userInput = input(prompt).strip()

        if userInput.startswith("-"):
            print("Negative numbers are not allowed. Please enter a positive number")
            continue

        try:
            return int(userInput) if wholeOnly else float(userInput)
        except ValueError:
            kind = "a whole number" if wholeOnly else "a number"
            print(f"Characters and spaces are not allowed. Please enter {kind}")

def formatProduct(productId, item):
    return (f"ID: {productId} | Name: {item['name']} | "
            f"Price: ${item['price']:.2f} | Stock: {item['stock']}")


def displayProducts(inventory):
    print("Current Inventory")
    print("------------------------------------------------")
    if not inventory:
        print("No products in inventory.")
    for productId, item in inventory.items():
        print(formatProduct(productId, item))
    print("------------------------------------------------")


def addProduct(inventory):
    print("Add New Product")
    while True:
        productId = getNonEmptyInput("Product ID: ").upper()
        if productId in inventory:
            print("That Product ID already exists. Please use a different ID.")
        else:
            break

    name = getNonEmptyInput("Product Name: ")
    price = getValidNumber("Price: ")
    stock = getValidNumber("Stock Quantity: ", wholeOnly=True)

    inventory[productId] = {"name": name, "price": price, "stock": stock}
    print("Product added successfully!")


def updateStock(inventory):
    print("Update Stock")
    productId = getNonEmptyInput("Product ID: ").upper()
    if productId not in inventory:
        print("Product not found.")
        return False

    item = inventory[productId]
    print(f"Current stock for {item['name']}: {item['stock']}")
    item["stock"] = getValidNumber("New Stock Quantity: ", wholeOnly=True)
    print("Stock updated successfully!")
    return True


def searchProduct(inventory):
    print("Search Product")
    term = getNonEmptyInput("Enter Product ID or Name: ").lower()
    matches = [
        (productId, item) for productId, item in inventory.items()
        if term in productId.lower() or term in item["name"].lower()
    ]

    print("------------------------------------------------")
    if matches:
        for productId, item in matches:
            print(formatProduct(productId, item))
    else:
        print("No matching products found.")
    print("------------------------------------------------")


def printMenu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = loadInventory()
    unsavedChanges = False

    while True:
        printMenu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            displayProducts(inventory)

        elif choice == "2":
            addProduct(inventory)
            unsavedChanges = True

        elif choice == "3":
            if updateStock(inventory):
                unsavedChanges = True

        elif choice == "4":
            searchProduct(inventory)

        elif choice == "5":
            saveInventory(inventory)
            unsavedChanges = False
            print("Inventory saved to inventory.json")

        elif choice == "6":
            if unsavedChanges:
                answer = input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower()
                if answer == "y":
                    saveInventory(inventory)
                    print("Inventory has been saved to inventory.json")
            print("Thank you for using Inventory Management System")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


main()