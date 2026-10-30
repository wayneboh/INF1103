from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    TYPE = "physical"
    BASE_SHIPPING_COST = 10.00
    COST_PER_KG = 5.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "Physical product: requires storage and physical shipping."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_COST + self.COST_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, product_id, data):
        return cls(product_id, data["name"], data["price"],
                   data["stock"], data["weight"])