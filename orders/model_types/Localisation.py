"""
Classe représentant la localisation
(pour la livraison de la commande)

"""

from pydantic import BaseModel


class Localisation(BaseModel):
    localisation_id: int
    address: str
    city: str
    postal_code: int


