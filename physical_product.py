from can_be_shipped import CanBeShipped
from product import Product, ProductData
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    TYPE: str = "physical"
    BASE_SHIPPING_COST: float = 5.00
    COST_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Physical product: requires storage and physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_COST + self.COST_PER_KG * self.__weight

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data