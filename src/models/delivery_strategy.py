from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    """Абстрактный класс стратегии доставки (OCP)"""

    @abstractmethod
    def calculate_cost(self, distance: float) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class StandardDelivery(DeliveryStrategy):
    """Стандартная доставка"""

    def calculate_cost(self, distance: float) -> float:
        return distance * 10

    def get_name(self) -> str:
        return "Стандартная доставка"


class ExpressDelivery(DeliveryStrategy):
    """Экспресс доставка"""

    def calculate_cost(self, distance: float) -> float:
        return distance * 20

    def get_name(self) -> str:
        return "Экспресс доставка"


class FreeDelivery(DeliveryStrategy):
    """Бесплатная доставка"""

    def calculate_cost(self, distance: float) -> float:
        return 0

    def get_name(self) -> str:
        return "Бесплатная доставка"