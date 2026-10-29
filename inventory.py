class Inventory:

    def __init__(self):
        self.__products = {}  # product_id -> Product

    def add_product(self, product):
        if product.product_id in self.__products:
            return False
        self.__products[product.product_id] = product
        return True

    def has_product(self, product_id):
        return product_id in self.__products

    def get_product(self, product_id):
        return self.__products.get(product_id)

    def search_product(self, term):
        term = term.lower()
        return [
            product for product in self.__products.values()
            if term in product.product_id.lower() or term in product.name.lower()
        ]

    def get_all_products(self):
        return list(self.__products.values())

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products.values():
            product.display_information()
        print("------------------------------------------------")