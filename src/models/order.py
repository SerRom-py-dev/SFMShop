from src.models.exceptions import InvalidOrderError


class Order:
    """Класс заказа с магическими методами"""

    def __init__(self, user, products, order_id=None):
        if not products or len(products) == 0:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")
        self.user = user
        self.products = products
        self.order_id = order_id
        self.total = self.calculate_total()

    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.get_total_price()
        return total

    # Магические методы
    def __len__(self):
        """Количество товаров в заказе"""
        return len(self.products)

    def __contains__(self, item):
        """Проверка наличия товара в заказе"""
        return item in self.products

    def __add__(self, other):
        """Объединение двух заказов"""
        if not isinstance(other, Order):
            raise TypeError("Можно объединять только заказы")
        new_products = self.products + other.products
        return Order(self.user, new_products, self.order_id)

    def __lt__(self, other):
        """Сравнение заказов по ID для сортировки"""
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id < other.order_id

    def __eq__(self, other):
        """Сравнение заказов по ID"""
        if not isinstance(other, Order):
            return False
        return self.order_id == other.order_id

    def __str__(self):
        user_name = self.user.name if hasattr(self.user, 'name') else str(self.user)
        order_num = f"Заказ #{self.order_id}" if self.order_id else "Заказ"
        return f"{order_num} на сумму {self.total} руб. (Пользователь: {user_name})"

    def __repr__(self):
        return f"Order(order_id={self.order_id}, total={self.total})"