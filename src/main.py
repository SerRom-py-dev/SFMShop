from src.models.payment import CardPayment, PayPalPayment
from src.models.order import Order
from src.models.product import Product
from src.models.user import User
from src.models.order_factory import OrderFactory, OrderCalculator
from src.models.delivery_strategy import StandardDelivery, ExpressDelivery, FreeDelivery
from src.models.metaclasses import ModelRegistryMeta
from src.models.exceptions import NegativePriceError


def process_advanced_order_system():
    """Демонстрация всех концепций ООП"""

    # 1. Создание пользователя и продуктов (Метакласс + Дескрипторы)
    print("\n1. МЕТАКЛАСС + ДЕСКРИПТОРЫ")
    print("-" * 40)

    user = User("Иван Иванов", "ivan@mail.com")
    print(user.get_info())

    laptop = Product("Ноутбук", 50000, 1)
    mouse = Product("Мышь", 500, 2)
    keyboard = Product("Клавиатура", 1500, 1)

    print(f"\n  {laptop}")
    print(f"  {mouse}")
    print(f"  {keyboard}")

    # Кэшированное свойство
    print(f"\n  Первый вызов total_value:")
    print(f"  Ноутбук total_value = {laptop.total_value}")
    print(f"  Второй вызов total_value (из кэша):")
    print(f"  Ноутбук total_value = {laptop.total_value}")

    # Валидация дескриптора
    print(f"\n  Проверка валидации дескриптора:")
    try:
        bad_product = Product("Плохой товар", -100, 1)
    except NegativePriceError as e:
        print(f"  [OK] Ошибка поймана: {e}")

    # 2. Реестр метакласса
    print("\n2. РЕЕСТР МЕТАКЛАССА")
    print("-" * 40)
    registry = ModelRegistryMeta.get_registry()
    print(f"  Зарегистрированные классы: {list(registry.keys())}")

    # to_dict через метакласс
    user_dict = user.to_dict()
    print(f"  User.to_dict(): {user_dict}")

    # 3. Factory Pattern
    print("\n3. FACTORY PATTERN")
    print("-" * 40)
    products = [laptop, mouse, keyboard]

    order1 = OrderFactory.create_order(1, products, user)
    print(f"  Создан: {order1}")

    order_from_dict = OrderFactory.create_order_from_dict({
        "order_id": 2,
        "products": [mouse, keyboard],
        "user": user
    })
    print(f"  Из словаря: {order_from_dict}")

    # 4. Магические методы Order
    print("\n4. МАГИЧЕСКИЕ МЕТОДЫ ORDER")
    print("-" * 40)

    print(f"  Количество товаров: {len(order1)}")  # __len__
    print(f"  Ноутбук в заказе: {laptop in order1}")  # __contains__
    print(f"  Мышь в заказе: {mouse in order1}")  # __contains__

    # Объединение заказов
    order3 = order1 + order_from_dict  # __add__
    print(f"  Объединенный заказ: {len(order3)} товаров")

    # Сортировка через __lt__
    orders = [order_from_dict, order1]
    sorted_orders = sorted(orders)  # __lt__
    print(f"  Сортировка заказов: {[o.order_id for o in sorted_orders]}")

    # 5. Strategy Pattern
    print("\n5. STRATEGY PATTERN (Доставка)")
    print("-" * 40)
    distance = 15.0

    for strategy in [StandardDelivery(), ExpressDelivery(), FreeDelivery()]:
        cost = strategy.calculate_cost(distance)
        print(f"  {strategy.get_name()} ({distance} км): {cost} руб.")

    # 6. Миксины + Полиморфизм платежей
    print("\n6. МИКСИНЫ + ПОЛИМОРФИЗМ ПЛАТЕЖЕЙ")
    print("-" * 40)

    payments = [
        CardPayment(order1.total, "4532015112830366"),
        PayPalPayment(order1.total, "ivan@mail.com")
    ]

    # Полиморфизм - один цикл для разных типов
    for payment in payments:
        result = payment.process_payment()  # Полиморфный вызов
        print(f"\n  {result}")
        payment.log("Платеж обработан")  # Миксин LoggableMixin
        print(f"  JSON: {payment.to_json()}")  # Миксин SerializableMixin

    # 7. MRO
    print("\n7. MRO (Method Resolution Order)")
    print("-" * 40)
    mro_names = [cls.__name__ for cls in CardPayment.mro()]
    print(f"  CardPayment MRO: {mro_names}")

    # 8. Калькулятор заказов
    print("\n8. КАЛЬКУЛЯТОР ЗАКАЗОВ")
    print("-" * 40)
    total = OrderCalculator.calculate_total(products)
    discounted = OrderCalculator.apply_discount(total, 10)
    print(f"  Сумма заказа: {total} руб.")
    print(f"  Скидка 10%: {discounted} руб.")

    return {
        "order": order1.to_dict() if hasattr(order1, 'to_dict') else str(order1),
        "delivery_cost": StandardDelivery().calculate_cost(distance),
        "user": user.to_dict(),
        "registry": list(ModelRegistryMeta.get_registry().keys())
    }


if __name__ == "__main__":
    result = process_advanced_order_system()
    print(f"\nРезультат: {result}")
