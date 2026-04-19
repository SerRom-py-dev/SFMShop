class PaymentProcessor:
    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "pending"

    def validate_payment(self):
        """Валидация платежа"""
        if self.amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if self.payment_method not in ["card", "paypal", "bank_transfer"]:
            raise ValueError("Неизвестный метод оплаты")
        return True

    def process_payment(self):
        """Обработка платежа - нарушает все принципы"""
        # Валидация
        self.validate_payment()

        # Обработка в зависимости от метода
        if self.payment_method == "card":
            # Логика для карты
            if self.amount > 10000:
                fee = self.amount * 0.02
            else:
                fee = self.amount * 0.03
            result = self._charge_card(self.amount + fee)
            if result:
                self.status = "completed"
                print(f"Платеж по карте обработан: {self.amount + fee}")
            else:
                self.status = "failed"
                raise ValueError("Ошибка обработки карты")

        elif self.payment_method == "paypal":
            # Логика для PayPal
            fee = self.amount * 0.035
            result = self._charge_paypal(self.amount + fee)
            if result:
                self.status = "completed"
                print(f"Платеж через PayPal обработан: {self.amount + fee}")
            else:
                self.status = "failed"
                raise ValueError("Ошибка обработки PayPal")

        elif self.payment_method == "bank_transfer":
            # Логика для банковского перевода
            fee = 50  # Фиксированная комиссия
            result = self._process_bank_transfer(self.amount + fee)
            if result:
                self.status = "completed"
                print(f"Банковский перевод обработан: {self.amount + fee}")
            else:
                self.status = "failed"
                raise ValueError("Ошибка банковского перевода")

        # Сохранение в БД
        self._save_to_database()

        # Отправка уведомления
        self._send_notification()

        return self.status

    def _charge_card(self, amount):
        """Зарядка карты"""
        print(f"Зарядка карты на сумму {amount}")
        return True

    def _charge_paypal(self, amount):
        """Зарядка PayPal"""
        print(f"Зарядка PayPal на сумму {amount}")
        return True

    def _process_bank_transfer(self, amount):
        """Обработка банковского перевода"""
        print(f"Банковский перевод на сумму {amount}")
        return True

    def _save_to_database(self):
        """Сохранение в БД"""
        print(f"Сохранение платежа {self.order_id} в MySQL")

    def _send_notification(self):
        """Отправка уведомления"""
        print(f"Отправка email о платеже {self.order_id}")