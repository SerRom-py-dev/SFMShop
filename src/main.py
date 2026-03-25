from src.models.product import Product
from src.models.user import User
from src.models.order import Order
from src.models.payment import CardPayment, PayPalPayment
from src.models.exceptions import ValidationError, SFMShopException


def process_order_system():
    # Создание пользователя
    user = User("Иван", "ivan@test.com")

    # Создание товаров
    product1 = Product("Ноутбук", 50000, 2)
    product2 = Product("Мышь", 1500, 3)

    # Создание заказа
    order = Order(user, [product1, product2])
    print(order)

    # Вычисление стоимости
    total = order.calculate_total()
    print("Общая стоимость заказа:", total)

    # Создание платежей
    payments = [
        CardPayment(1000, "1234 5678 9012 3456"),
        PayPalPayment(2000, "test@paypal.com")
    ]

    # Обработка платежей через полиморфизм
    for payment in payments:
        print(payment.process_payment())

    # Сортировка товаров
    sorted_products = sorted([product1, product2])
    for product in sorted_products:
        print(product)

    # Обработка ошибок
    try:
        product1.set_price(-1000)
    except ValidationError as e:
        print("Ошибка валидации:", e)


if __name__ == "__main__":
    process_order_system()