import csv
import json
import os

from bulk_discount import BulkDiscount
from discount_strategy import DiscountStrategy
from inventory import Inventory
from no_discount import NoDiscount
from order import Order
from percentage_discount import PercentageDiscount
from product_factory import ProductFactory
from student_discount import StudentDiscount
from supplier import Supplier

INVENTORY_FILE_NAME = "inventory.json"
DEFAULT_PRODUCTS_FILE = "products.csv"

DISCOUNT_OPTIONS: dict[str, tuple[str, DiscountStrategy]] = {
    "1": ("No discount", NoDiscount()),
    "2": ("10% off", PercentageDiscount(10)),
    "3": ("20 off orders of 200 or more", BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", StudentDiscount()),
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
            supplier = suppliers.get(item.get("supplier_id"))
            if supplier is None:
                print(f"Skipping {product_id}: unknown supplier.")
                continue
            try:
                product = ProductFactory.create_from_dict(product_id, item, supplier)
            except ValueError as error:
                print(f"Skipping {product_id}: {error}")
                continue
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, AttributeError):
        print("Could not read inventory.json, starting with an empty inventory.")
        return Inventory(), {}
    return inventory, suppliers


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type.strip(), product_id.strip().upper(),
                        name.strip(), float(price), int(stock), supplier)
                except ValueError as error:
                    print(f"Skipping row {reader.line_num}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {reader.line_num}: "
                          f"product ID {product.product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


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


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_product_type() -> str:
    while True:
        choice = input("Product type (1 = Physical, 2 = Digital): ").strip()
        if choice == "1":
            return ProductFactory.PHYSICAL
        if choice == "2":
            return ProductFactory.DIGITAL
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


def choose_discount() -> DiscountStrategy:
    print("Discount options:")
    for key, (label, _) in DISCOUNT_OPTIONS.items():
        print(f"{key}. {label}")
    while True:
        choice = input("Choose a discount: ").strip()
        if choice in DISCOUNT_OPTIONS:
            return DISCOUNT_OPTIONS[choice][1]
        print(f"Invalid choice. Please enter a number from 1 to {len(DISCOUNT_OPTIONS)}.")


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    print("Add New Product")
    while True:
        product_id = get_non_empty_input("Product ID: ").upper()
        if inventory.has_product(product_id):
            print("That Product ID already exists. Please use a different ID.")
        else:
            break

    product_type = get_product_type()
    name = get_non_empty_input("Product Name: ")
    price = get_positive_float("Price: ")
    stock = get_valid_number("Stock Quantity: ", whole_only=True)

    if product_type == ProductFactory.PHYSICAL:
        extra_value = get_valid_number("Weight (kg): ")
    else:
        extra_value = get_valid_number("Download Size (MB): ")

    supplier = get_supplier(suppliers)

    try:
        product = ProductFactory.create(product_type, product_id, name, price,
                                        stock, supplier, extra_value)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return False

    inventory.add_product(product)
    print("Product added successfully!")
    return True


def update_stock(inventory: Inventory) -> bool:
    print("Update Stock")
    product_id = get_non_empty_input("Product ID: ").upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return False

    print(f"Current stock for {product.name}: {product.stock}")
    try:
        product.update_stock(get_valid_number("New Stock Quantity: ", whole_only=True))
    except ValueError as error:
        print(f"Could not update stock: {error}")
        return False
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
    order = Order(get_non_empty_input("Order ID: ").upper(), choose_discount())

    while True:
        product_id = input("Product ID to add (press Enter to finish): ").strip().upper()
        if not product_id:
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        quantity = get_valid_number("Quantity: ", whole_only=True)
        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(f"Could not add item: {error}")
            continue
        print("Item added to order.")

    order.display_information()


def import_products(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    print("Import Products from CSV")
    path = input(f"CSV file path (press Enter for {DEFAULT_PRODUCTS_FILE}): ").strip()
    if not path:
        path = DEFAULT_PRODUCTS_FILE

    supplier = get_supplier(suppliers)
    count_before = len(inventory.products)
    load_products(path, inventory, supplier)
    return len(inventory.products) > count_before


def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Create Order")
    print("7. Import Products from CSV")
    print("8. Exit")
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
            if add_product(inventory, suppliers):
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
            if import_products(inventory, suppliers):
                unsaved_changes = True

        elif choice == "8":
            if unsaved_changes:
                answer = input("You have unsaved changes. Save before exiting? (y/n): ").strip().lower()
                if answer == "y":
                    save_inventory(inventory, suppliers)
                    print("Inventory has been saved to inventory.json")
            print("Thank you for using Inventory Management System")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()