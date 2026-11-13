from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (100 - self.__percentage) / 100