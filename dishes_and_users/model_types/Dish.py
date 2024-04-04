from pydantic import BaseModel


class Dish(BaseModel):
    """
    Represents a dish object.

    Attributes:
        id (int): The unique identifier for the dish.
        description (str): The description of the dish.
        price (float): The price of the dish.
    """
    id: int
    description: str
    price: float
