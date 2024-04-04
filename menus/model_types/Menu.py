from pydantic import BaseModel
from model_types.Dish import Dish


class Menu(BaseModel):
    id: int
    utilisateur_id: int
    dishes: list[Dish]
    date_creation: str
    date_modification: str
