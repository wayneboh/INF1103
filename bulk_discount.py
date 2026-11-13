from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total