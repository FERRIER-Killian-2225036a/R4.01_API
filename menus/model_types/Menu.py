"""
Menu Model Module
=================

This module defines the Menu model for the API.

Dependencies:
    - pydantic: Data validation and settings management using Python type annotations.

"""

from pydantic import BaseModel
from model_types.Dish import Dish


class Menu(BaseModel):
    """
    Represents a menu in the API.

    Attributes:
        id (int): The unique identifier for the menu.
        utilisateur_id (int): The identifier of the user associated with the menu.
        dishes (list[Dish]): The list of dishes included in the menu.
        date_creation (str): The date when the menu was created.
        date_modification (str): The date when the menu was last modified.

    """
    id: int
    utilisateur_id: int
    dishes: list[Dish]
    date_creation: str
    date_modification: str
