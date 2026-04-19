import json

class LoggableMixin:
    """Миксин для логирования"""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class SerializableMixin:
    """Миксин для сериализации в JSON"""
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)