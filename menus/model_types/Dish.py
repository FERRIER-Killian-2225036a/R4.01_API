from pydantic import BaseModel


class Dish(BaseModel):
    description: str
    price: float
