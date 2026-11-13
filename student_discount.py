from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):

    DISCOUNT_RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.DISCOUNT_RATE)