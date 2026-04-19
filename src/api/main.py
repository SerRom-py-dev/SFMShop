from fastapi import FastAPI
from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в SFMShop API"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Ноутбук", "price": 50000, "quantity": 10},
        {"id": 2, "name": "Мышь", "price": 1500, "quantity": 20},
        {"id": 3, "name": "Клавиатура", "price": 3000, "quantity": 15}
    ]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    # В реальном приложении здесь будет запрос к БД
    products = {
        1: {"id": 1, "name": "Ноутбук", "price": 50000, "quantity": 10},
        2: {"id": 2, "name": "Мышь", "price": 1500, "quantity": 20},
        3: {"id": 3, "name": "Клавиатура", "price": 3000, "quantity": 15}
    }
    return products.get(product_id, {"error": "Товар не найден"})

@app.post("/orders")
def create_order(order: OrderCreate):
    # В реальном приложении здесь будет создание заказа в БД
    return {
        "id": 5,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "message": "Заказ создан"
    }
