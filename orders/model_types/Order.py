"""
Classe représentant une commande

"""

from model_types.Localisation import *
from datetime import datetime


class Order(BaseModel):
    command_id: int
    menus_id: list[int]
    user_id: int
    localisation: Localisation
    price: float
    date: datetime

