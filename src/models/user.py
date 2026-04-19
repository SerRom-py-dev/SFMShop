from src.models.metaclasses import ModelRegistryMeta


class User(metaclass=ModelRegistryMeta):
    """Класс пользователя с метаклассом"""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_info(self):
        return f"Пользователь: {self.name}, Email: {self.email}"

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"