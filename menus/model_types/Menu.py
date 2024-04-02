from pydantic import BaseModel
import Dish 


class Menu(BaseModel):
    id: int
    utilisateur_id: int
    plats: list[Dish]
    date_creation: date
    date_modification: date
