"""
Fichier permettant la gestion des URL de la classe Order

"""

from data_access.Data import Data
from orders.model_types.Order import Order
from fastapi import APIRouter

router = APIRouter()
data_instance: Data | None = None


def setup_routes(app):
    app.include_router(router)


def data_transmission(data: Data):
    """
    transmet le contexte a la base de donnée

    :param data:
    """
    global data_instance
    if data_instance is None:
        data_instance = data


@router.get("/order/{order_id}")
def read_order(order_id: int):
    result = data_instance.order_CRUD(data_instance, "READ", None, order_id)
    return {"Lecture Commande", result}


@router.post("/order")
def create_order(order: Order):
    """
    route permettant de creer une commande

    :param order: les informations de la commande
    """
    return {""}


@router.put("/order/{order_id}")
def update_order(order_id: int, order: Order):
    """
    route permettant de mettre à jour une commande

    :param order_id: l'identifiant de la commande à modifier
    :param order: les nouvelles informations de la commande
    """
    pass


@router.delete("/order/{order_id}")
def delete_order(order_id: int):
    """
    route permettant de supprimer une commande

    :param order_id: l'identifiant de la commande à supprimer
    """
    pass
