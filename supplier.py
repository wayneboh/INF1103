class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, supplier_id: str, data: dict[str, str]) -> "Supplier":
        return cls(supplier_id, data["name"], data["contact_email"])