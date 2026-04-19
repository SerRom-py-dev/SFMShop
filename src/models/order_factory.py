from src.models.order import Order
from src.models.exceptions import InvalidOrderError


class OrderValidator:
    """Валидатор заказов (SRP)"""

    @staticmethod
    def validate(order):
        if not order.products:
            raise InvalidOrderError("Заказ не содержит товаров")
        if order.total <= 0:
            raise InvalidOrderError("Сумма заказа должна быть положительной")


class OrderCalculator:
    """Калькулятор заказов (SRP)"""

    @staticmethod
    def calculate_total(products):
        return sum(p.get_total_price() for p in products)

    @staticmethod
    def apply_discount(total, discount_percent):
        if not 0 <= discount_percent <= 100:
            raise ValueError("Скидка должна быть от 0 до 100")
        return total * (1 - discount_percent / 100)


class OrderFactory:
    """Фабрика для создания заказов (Factory Pattern)"""

    @staticmethod
    def create_order(order_id, products, user):
        order = Order(user, products, order_id)
        OrderValidator.validate(order)
        return order

    @classmethod
    def create_order_from_dict(cls, data):
        """Создание заказа из словаря"""
        return cls.create_order(
            data["order_id"],
            data["products"],
            data["user"]
        )