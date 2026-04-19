from abc import ABC, abstractmethod
from src.models.mixins import LoggableMixin, SerializableMixin


class Payment(ABC):
    """Абстрактный базовый класс для платежей"""

    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def process_payment(self):
        pass


class CardPayment(Payment, LoggableMixin, SerializableMixin):
    """Оплата картой с миксинами логирования и сериализации"""

    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.__card_number = card_number
        self.log(f"Создан платеж картой на сумму {amount} руб.")

    def process_payment(self):
        self.log("Обработка платежа картой")
        masked_card = "**** " + self.__card_number[-4:]
        return f"Оплата картой {masked_card}: {self.amount} руб."

    def to_dict(self):
        return {
            "type": "CardPayment",
            "amount": self.amount,
            "card": "**** " + self.__card_number[-4:]
        }


class PayPalPayment(Payment, LoggableMixin, SerializableMixin):
    """Оплата PayPal с миксинами логирования и сериализации"""

    def __init__(self, amount, email):
        super().__init__(amount)
        self.email = email
        self.log(f"Создан PayPal платеж на сумму {amount} руб.")

    def process_payment(self):
        self.log(f"Обработка PayPal платежа для {self.email}")
        return f"Оплата PayPal ({self.email}): {self.amount} руб."

    def to_dict(self):
        return {
            "type": "PayPalPayment",
            "amount": self.amount,
            "email": self.email
        }