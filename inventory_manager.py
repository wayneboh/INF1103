import json
import os

from inventory import Inventory
from product import Product

INVENTORY_FILE_NAME = "inventory.json"


def save_inventory(inventory):
    data = {
        product.product_id: {
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        }
        for product in inventory.get_all_products()
    }
    with open(INVENTORY_FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def load_inventory():
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE_NAME):
        print("No inventory.json found, creating a new file.")
        save_inventory(inventory)
        return inventory

    print("inventory.json found.")
    try:
        with open(INVENTORY_FILE_NAME, "r") as file:
            data = json.load(file)
        for product_id, item in data.items():
            inventory.add_product(
                Product(product_id, item["name"], item["price"], item["stock"])
            )
        print("Inventory loaded successfully.")
    except (ValueError, IOError, KeyError, TypeError, AttributeError):
        print("Could not read inventory.json, starting with an empty inventory.")
        return Inventory()
    return inventory


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_number(prompt, whole_only=False):
    while True:
        user_input = input(prompt).strip()

        if user_input.startswith("-"):
            print("Negative numbers are not allowed. Please enter a positive number")
            continue

        try:
            return int(user_input) if whole_only else float(user_input)
        except ValueError:
            kind = "a whole number" if whole_only else "a number"
            print(f"Characters and spaces are not allowed. Please enter {kind}")

def add_product(inventory):
    print("Add New Product")
    while True:
        product_id = get_non_empty_input("Product ID: ").upper()
        if inventory.has_product(product_id):
            print("That Product ID already exists. Please use a different ID.")
        else:
            break

    name = get_non_empty_input("Product Name: ")
    price = get_valid_number("Price: ")
    stock = get_valid_number("Stock Quantity: ", whole_only=True)

    inventory.add_product(Product(product_id, name, price, stock))
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    product_id = get_non_empty_input("Product ID: ").upper()
    product = inventory.get_product(product_id)
    if product is None:
        print("Product not found.")
        return False

    print(f"Current stock for {product.name}: {product.stock}")
    product.update_stock(get_valid_number("New Stock Quantity: ", whole_only=True))
    print("Stock updated successfully!")
    return True


def search_product(inventory):
    print("Search Product")
    term = get_non_empty_input("Enter Product ID or Name: ")
    matches = inventory.search_product(term)

    print("------------------------------------------------")
    if matches:
        for product in matches:
            product.display_information()
    else:
        print("No matching products found.")
    print("------------------------------------------------")


def print_menu():
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

    inventory = load_inventory()
    unsaved_changes = False

    while True:
        print_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product(inventory)
            unsaved_changes = True

        elif choice == "3":
            if update_stock(inventory):
                unsaved_changes = True

        elif choice == "4":
            search_product(inventory)

        elif choice == "5":
            save_inventory(inventory)
            unsaved_changes = False
            print("Inventory saved to inventory.json")

        elif choice == "6":
            if unsaved_changes:
                answer = input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower()
                if answer == "y":
                    save_inventory(inventory)
                    print("Inventory has been saved to inventory.json")
            print("Thank you for using Inventory Management System")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()