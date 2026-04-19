class ShoppingCart:

    def __init__(self):
        self.items = []

    def __add__(self, item):
        new_cart = ShoppingCart()
        new_cart.items = self.items.copy()
        new_cart.items.append(item)
        return new_cart

    def __sub__(self, item):
        new_cart = ShoppingCart()
        new_cart.items = [i for i in self.items if i != item]
        return new_cart

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return f"Корзина: {len(self.items)} товаров"


cart = ShoppingCart()
cart = cart + "Ноутбук"
cart = cart + "Мышь"
cart = cart + "Клавиатура"

print(len(cart))  # 3

for item in cart:
    print(item)
