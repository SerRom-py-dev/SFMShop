class OrderValidator:
    """Класс для валидации заказов (Single Responsibility Principle)"""
    
    @staticmethod
    def validate(order) -> bool:
        """Валидировать заказ"""
        if not order.items:
            raise ValueError("Заказ не может быть пустым")
        if not order.user:
            raise ValueError("Заказ должен иметь пользователя")
        for item in order.items:
            if item.quantity <= 0:
                raise ValueError("Количество товара должно быть положительным")
        return True
    
    @staticmethod
    def validate_total(total: float) -> bool:
        """Валидировать сумму заказа"""
        if total < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")
        return True
