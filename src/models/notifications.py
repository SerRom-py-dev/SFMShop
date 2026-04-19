from abc import ABC, abstractmethod

class Notification(ABC):
    """Абстрактный класс для системы уведомлений"""
    
    def __init__(self, recipient: str, message: str):
        self.recipient = recipient
        self.message = message
    
    @abstractmethod
    def send(self) -> bool:
        """Отправить уведомление"""
        pass

class EmailNotification(Notification):
    """Email уведомление"""
    
    def send(self) -> bool:
        """Отправка email уведомления"""
        print(f"Отправка email на {self.recipient}: {self.message}")
        return True

class SMSNotification(Notification):
    """SMS уведомление"""
    
    def send(self) -> bool:
        """Отправка SMS уведомления"""
        print(f"Отправка SMS на {self.recipient}: {self.message}")
        return True
