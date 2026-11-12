import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

INVENTORY_FILE_NAME = "inventory.json"

PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    data = {
        "suppliers": {
            supplier_id: supplier.to_dict()
            for supplier_id, supplier in suppliers.items()
        },
        "products": {
            product.product_id: product.to_dict()
            for product in inventory.products
        },
    }
    with open(INVENTORY_FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE_NAME):
        print("No inventory.json found, creating a new file.")
        save_inventory(inventory, suppliers)
        return inventory, suppliers

    print("inventory.json found.")
    try:
        with open(INVENTORY_FILE_NAME, "r") as file:
            data = json.load(file)

        if data and "products" not in data:
            print("inventory.json uses an older format without suppliers, "
                  "starting with an empty inventory.")
            return inventory, suppliers

        for supplier_id, item in data.get("suppliers", {}).items():
            suppliers[supplier_id] = Supplier.from_dict(supplier_id, item)

        for product_id, item in data.get("products", {}).items():
            product_class = PRODUCT_TYPES.get(item.get("type"))
            supplier = suppliers.get(item.get("supplier_id"))
            if product_class is None or supplier is None:
                print(f"Skipping {product_id}: unknown product type or supplier.")
                continue
            inventory.add_product(product_class.from_dict(product_id, item, supplier))
        print("Inventory loaded successfully.")
    except (ValueError, IOError, KeyError, TypeError, AttributeError):
        print("Could not read inventory.json, starting with an empty inventory.")
        return Inventory(), {}
    return inventory, suppliers


def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_number(prompt: str, whole_only: bool = False) -> int | float:
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


def get_product_type() -> str:
    while True:
        choice = input("Product type (1 = Physical, 2 = Digital): ").strip()
        if choice == "1":
            return PhysicalProduct.TYPE
        if choice == "2":
            return DigitalProduct.TYPE
        print("Invalid choice. Please enter 1 or 2.")


def get_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id = get_non_empty_input("Supplier ID: ").upper()
    existing = suppliers.get(supplier_id)
    if existing is not None:
        print("Using existing supplier:")
        existing.display_information()
        return existing

    print("New supplier, please enter the details.")
    name = get_non_empty_input("Supplier Name: ")
    contact_email = get_non_empty_input("Supplier Contact Email: ")
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers[supplier_id] = supplier
    return supplier


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("Add New Product")
    while True:
        product_id = get_non_empty_input("Product ID: ").upper()
        if inventory.has_product(product_id):
            print("That Product ID already exists. Please use a different ID.")
        else:
            break

    product_type = get_product_type()
    name = get_non_empty_input("Product Name: ")
    price = get_valid_number("Price: ")
    stock = get_valid_number("Stock Quantity: ", whole_only=True)

    product: Product
    if product_type == PhysicalProduct.TYPE:
        weight = get_valid_number("Weight (kg): ")
        supplier = get_supplier(suppliers)
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_valid_number("Download Size (MB): ")
        supplier = get_supplier(suppliers)
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> bool:
    print("Update Stock")
    product_id = get_non_empty_input("Product ID: ").upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return False

    print(f"Current stock for {product.name}: {product.stock}")
    product.update_stock(get_valid_number("New Stock Quantity: ", whole_only=True))
    print("Stock updated successfully!")
    return True


def search_product(inventory: Inventory) -> None:
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


def create_order(inventory: Inventory) -> None:
    print("Create Order")
    order = Order(get_non_empty_input("Order ID: ").upper())

    while True:
        product_id = input("Product ID to add (press Enter to finish): ").strip().upper()
        if not product_id:
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        quantity = get_valid_number("Quantity: ", whole_only=True)
        if quantity == 0:
            print("Quantity must be at least 1.")
            continue

        order.add_order_line(product, quantity)
        print("Item added to order.")

    order.display_information()


def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Create Order")
    print("7. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory, suppliers = load_inventory()
    unsaved_changes = False

    while True:
        print_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all_products()

        elif choice == "2":
            add_product(inventory, suppliers)
            unsaved_changes = True

        elif choice == "3":
            if update_stock(inventory):
                unsaved_changes = True

        elif choice == "4":
            search_product(inventory)

        elif choice == "5":
            save_inventory(inventory, suppliers)
            unsaved_changes = False
            print("Inventory saved to inventory.json")

        elif choice == "6":
            create_order(inventory)

        elif choice == "7":
            if unsaved_changes:
                answer = input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower()
                if answer == "y":
                    save_inventory(inventory, suppliers)
                    print("Inventory has been saved to inventory.json")
            print("Thank you for using Inventory Management System")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()