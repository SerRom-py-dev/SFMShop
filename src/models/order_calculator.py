class OrderCalculator:
    """Класс для расчетов заказов (Single Responsibility Principle)"""
    
    @staticmethod
    def calculate_total(order) -> float:
        """Рассчитать общую стоимость заказа"""
        total = 0
        for item in order.items:
            total += item.price * item.quantity
        return total
    
    @staticmethod
    def calculate_discount(total: float, discount_rate: float) -> float:
        """Рассчитать скидку"""
        return total * discount_rate
    
    @staticmethod
    def calculate_final_total(total: float, discount: float) -> float:
        """Рассчитать итоговую стоимость со скидкой"""
        return total - discount
