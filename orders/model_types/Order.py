"""
Classe représentant une commande

"""

from pydantic import BaseModel
from model_types.Localisation import Localisation
from datetime import datetime


class Order(BaseModel):
    command_id: int
    menus_id: list[int]
    user_id: int
    localisation: Localisation
    price: float
    date: datetime

