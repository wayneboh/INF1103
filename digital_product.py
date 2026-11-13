from product import Product, ProductData
from supplier import Supplier


class DigitalProduct(Product):

    TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally by download, no shipping needed."

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data