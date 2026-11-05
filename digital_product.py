from product import Product


class DigitalProduct(Product):

    TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "Digital product: delivered digitally by download, no shipping needed."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, product_id, data):
        return cls(product_id, data["name"], data["price"],
                   data["stock"], data["download_size"])