from src.models.exceptions import NegativePriceError, InsufficientStockError
from src.models.descriptors import PositiveNumber, CachedProperty
from src.models.metaclasses import ModelRegistryMeta


class Product(metaclass=ModelRegistryMeta):
    """Класс продукта с дескрипторами и метаклассом"""

    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, name, price, quantity):
        if price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self.name = name
        self.price = price
        self.quantity = quantity

    @CachedProperty
    def total_value(self):
        """Вычисляемое свойство с кэшированием"""
        print("  [CachedProperty] Вычисление total_value...")
        return self.price * self.quantity

    def get_total_price(self):
        return self.price * self.quantity

    def sell(self, amount):
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Недостаточно товара. На складе: {self.quantity}, требуется: {amount}"
            )
        self.quantity -= amount

    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price