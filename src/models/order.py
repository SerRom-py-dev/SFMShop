from src.models.product import Product

class Order:
    def __init__(self, user, products):
        self.user = user
        self.products = products

    def add_product(self, product):
        if isinstance(product, Product):
            self.products.append(product)

    def calculate_total(self):
        total = 0
        for product in self.products:
            total = total + product.price * product.quantity
        return total

    def __str__(self):
        return f"Заказ пользователя {self.user.name} на сумму {self.calculate_total()} руб."