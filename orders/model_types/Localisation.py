from pydantic import BaseModel


class Localisation(BaseModel):
    localisation_id: int
    adress: str
    city: str
    postal_code: int
