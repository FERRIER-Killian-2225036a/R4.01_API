from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a user object.

    Attributes:
        id (int): The unique identifier for the user.
        login (str): The login username of the user.
        password (str): The password of the user.
    """
    id: int
    login: str
    password: str
