class PositiveNumber:
    """Дескриптор для валидации положительных чисел"""
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Значение '{self.public_name}' должно быть числом")
        if value < 0:
            raise ValueError(f"Значение '{self.public_name}' должно быть положительным")
        setattr(obj, self.private_name, value)

class CachedProperty:
    """Дескриптор для кэширования вычисляемых свойств"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.func(obj)
        return obj.__dict__[self.name]
