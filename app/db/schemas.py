from pydantic import BaseModel

"""
Структура БД - на Ваше усмотрение, но в ней обязательно должны храниться:
·      Название товара
·      Артикул
·      Цена
·      Рейтинг товара
·      Суммарное количество товара НА ВСЕХ СКЛАДАХ на момент запроса
"""


class ProductCreate(BaseModel):
    artikul: int


class ProductResponse(BaseModel):
    artikul: int
    name: str
    price: float
    rating: float
    total_quantity: int

    class Config:
        orm_mode = True
