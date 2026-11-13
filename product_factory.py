from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product, ProductData
from supplier import Supplier


class ProductFactory:

    PHYSICAL: str = PhysicalProduct.TYPE
    DIGITAL: str = DigitalProduct.TYPE

    EXTRA_FIELDS: dict[str, str] = {
        PHYSICAL: "weight",
        DIGITAL: "download_size",
    }

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        if product_type == ProductFactory.PHYSICAL:
            return PhysicalProduct(product_id, name, price, stock, supplier, extra_value)
        elif product_type == ProductFactory.DIGITAL:
            return DigitalProduct(product_id, name, price, stock, supplier, extra_value)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_from_dict(product_id: str, data: ProductData,
                         supplier: Supplier) -> Product:
        product_type = str(data.get("type"))
        if product_type not in ProductFactory.EXTRA_FIELDS:
            raise ValueError(f"Unknown product type: {product_type}")
        extra_value = data[ProductFactory.EXTRA_FIELDS[product_type]]
        return ProductFactory.create(product_type, product_id, data["name"],
                                     data["price"], data["stock"], supplier,
                                     extra_value)