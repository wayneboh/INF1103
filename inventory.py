from product import Product


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        if self.has_product(product.product_id):
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def has_product(self, product_id: str) -> bool:
        return self.find_product(product_id) is not None

    def search_product(self, term: str) -> list[Product]:
        term = term.lower()
        return [
            product for product in self.__products
            if term in product.product_id.lower() or term in product.name.lower()
        ]

    def display_all_products(self) -> None:
        print("Current Inventory")
        print("------------------------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("------------------------------------------------")