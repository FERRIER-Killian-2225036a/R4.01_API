"""
Dish Model Module
=================

This module defines the Dish model for the API.

Dependencies:
    - pydantic: Data validation and settings management using Python type annotations.

"""

from pydantic import BaseModel


class Dish(BaseModel):
    """
    Represents a dish in the API.

    Attributes:
        description (str): The description of the dish.
        price (float): The price of the dish.

    """
    description: str
    price: float
