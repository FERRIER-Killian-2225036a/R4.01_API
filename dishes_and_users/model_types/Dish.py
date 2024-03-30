from pydantic import BaseModel


class Dish(BaseModel):
    id: int
    description: str
    price: float
