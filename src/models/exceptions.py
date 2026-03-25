class SFMShopException(Exception):
    """Базовое исключение для проекта SFMShop"""
    pass


class ValidationError(SFMShopException):
    """Ошибка валидации данных"""
    pass


class BusinessLogicError(SFMShopException):
    """Ошибка бизнес-логики"""
    pass


class DatabaseError(SFMShopException):
    pass


class NegativePriceError(ValidationError):
    """Отрицательная цена"""
    pass


class InsufficientStockError(BusinessLogicError):
    """Недостаточно товара"""
    pass


class InvalidOrderError(BusinessLogicError):
    """Невалидный заказ"""
    pass

