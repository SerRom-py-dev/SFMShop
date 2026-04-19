from abc import ABC, abstractmethod

# ДЕСКРИПТОРЫ

class Positive:
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, owner):
        return getattr(obj, self.name, 0) if obj else self

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError("Должно быть положительным")
        setattr(obj, self.name, value)


class NonEmpty:
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, owner):
        return getattr(obj, self.name, '') if obj else self

    def __set__(self, obj, value):
        if not str(value).strip():
            raise ValueError("Не может быть пустым")
        setattr(obj, self.name, str(value).strip())


# МИКСИН

class Logger:
    def log(self, msg):
        print(f"[{self.__class__.__name__}] {msg}")


class Product:
    name = NonEmpty()
    price = Positive()

    def __init__(self, id, name, price):
        self.id, self.name, self.price = id, name, price

    def __repr__(self):
        return f"{self.name}: {self.price}"

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id


class OrderItem:
    qty = Positive()

    def __init__(self, product, qty):
        self.product, self.qty = product, qty

    @property
    def total(self):
        return self.product.price * self.qty

    def __repr__(self):
        return f"{self.product.name} x {self.qty} = {self.total}"


class Order(Logger):
    def __init__(self, id, customer):
        self.id, self.customer, self.items, self.status = id, customer, [], "new"
        self.log(f"Заказ {id} создан")

    def add(self, product, qty=1):
        self.items.append(OrderItem(product, qty))

    @property
    def total(self):
        return sum(i.total for i in self.items)

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        new = Order(self.id, self.customer)
        new.items = self.items + other.items
        return new

    def __iadd__(self, product):
        self.add(product, 1) if isinstance(product, Product) else self.items.append(product)
        return self

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, product):
        return any(i.product == product for i in self.items)

    def __str__(self):
        return f"Заказ #{self.id} ({self.customer}): {len(self)}, {self.total}"


# ПЛАТЕЖИ

class Payment(ABC, Logger):
    def __init__(self, amount):
        self.amount, self.status, self.id = amount, "pending", None

    @abstractmethod
    def validate(self): pass

    @abstractmethod
    def process(self): pass

    @abstractmethod
    def refund(self): pass

    def _done(self):
        self.status = "completed"
        self.log(f"Платеж {self.amount} завершен")


class CardPayment(Payment):
    def __init__(self, amount, card, cvv):
        super().__init__(amount)
        self.card, self.cvv = card, cvv

    def validate(self):
        return len(self.cvv) == 3 and len(self.card) >= 13

    def process(self):
        if not self.validate():
            return False
        self.id = f"CC-{id(self)}"
        self._done()
        return True

    def refund(self):
        if self.status == "completed":
            self.status = "refunded"
            return True
        return False


class PayPal(Payment):
    def __init__(self, amount, email):
        super().__init__(amount)
        self.email = email

    def validate(self):
        return '@' in self.email

    def process(self):
        if not self.validate():
            return False
        self.id = f"PP-{id(self)}"
        self._done()
        return True

    def refund(self):
        if self.status == "completed":
            self.status = "refunded"
            return True
        return False


class Crypto(Payment):
    def __init__(self, amount, wallet):
        super().__init__(amount)
        self.wallet = wallet

    def validate(self):
        return len(self.wallet) >= 26

    def process(self):
        if not self.validate():
            return False
        self.id = f"CRYPTO-{id(self)}"
        self._done()
        return True

    def refund(self):
        if self.status == "completed":
            self.status = "refunded"
            return True
        return False


class Processor(Logger):
    def pay(self, order, payment):
        if payment.amount < order.total:
            return False
        if payment.process():
            order.status = "paid"
            return True
        return False

    def refund(self, order, payment):
        if payment.refund():
            order.status = "refunded"
            return True
        return False


# DEMO

def main():

    # Продукты
    print("\n1. Продукты:")
    laptop = Product(1, "Ноутбук", 50000)
    mouse = Product(2, "Мышь", 500)
    keyboard = Product(3, "Клавиатура", 1500)
    print(f"  {laptop}\n  {mouse}\n  {keyboard}")

    # Заказ
    print("\n2. Заказ:")
    order = Order(101, "Иван")
    order.add(laptop, 1)
    order.add(mouse, 2)
    order += keyboard  # __iadd__

    print(f"  Позиций: {len(order)}")  # __len__
    print(f"  Сумма: {order.total}")
    print(f"  Ноутбук есть: {laptop in order}")  # __contains__
    print(f"  {order}")  # __str__

    # Итерация
    print("\n3. Товары:")
    for item in order:  # __iter__
        print(f"  {item}")

    # Объединение
    print("\n4. Объединение:")
    order2 = Order(102, "Иван")
    order2.add(Product(4, "Монитор", 15000), 1)
    combined = order + order2  # __add__
    print(f"  {combined}")

    # Платежи
    print("\n5. Платежи:")
    proc = Processor()

    print("\n  Карта:")
    card = CardPayment(order.total, "4532015112830366", "123")
    print(f"  Успех: {proc.pay(order, card)}")
    print(f"  Статус: {order.status}")

    print("\n  PayPal:")
    order3 = Order(103, "Петр")
    order3.add(mouse, 1)
    pp = PayPal(order3.total, "user@mail.com")
    proc.pay(order3, pp)

    print("\n  Крипто:")
    order4 = Order(104, "Сергей")
    order4.add(keyboard, 1)
    crypto = Crypto(order4.total, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    proc.pay(order4, crypto)

    # Возврат
    print("\n6. Возврат:")
    proc.refund(order, card)
    print(f"  Статус: {card.status}")

    # Валидация
    print("\n7. Валидация:")
    try:
        Product(5, "", -100)
    except ValueError as e:
        print(f"   {e}")


if __name__ == "__main__":
    main()