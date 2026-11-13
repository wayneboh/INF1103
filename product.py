from abc import ABC, abstractmethod

from supplier import Supplier

ProductData = dict[str, str | float | int]


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__validate_stock(stock)
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    @staticmethod
    def __validate_stock(quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

    def update_stock(self, quantity: int) -> None:
        self.__validate_stock(quantity)
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print(f"    Supplier: {self.__supplier.name} "
              f"({self.__supplier.contact_email})")

    def to_dict(self) -> ProductData:
        return {
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.supplier_id,
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass