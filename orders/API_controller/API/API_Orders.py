"""
Fichier permettant la gestion des URL de la classe Order

"""
from starlette.responses import JSONResponse

from data_access.Data import Data
from model_types.Order import Order
from fastapi import APIRouter, HTTPException

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

@router.get("/")
def welcome():
    return {"message": "Bienvenue sur l'API"}

@router.get("/order/{order_id}")
def read_order(order_id: int):
    try:
        order = data_instance.order_CRUD("READ", object_id=order_id)
        return {"message": "La commande a été lue avec succès. ", "Commande": order}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.post("/order")
def create_order(order: Order):
    """
    route permettant de creer une commande

    :param order: les informations de la commande
    """
    try:
        data_instance.order_CRUD("CREATE", object_instance=order)
        return {"message": "La commande a été créée"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/order/{order_id}")
def update_order(order_id: int, order: Order):
    """
    route permettant de mettre à jour une commande

    :param order_id: l'identifiant de la commande à modifier
    :param order: les nouvelles informations de la commande
    """
    try:
        data_instance.order_CRUD("UPDATE", object_id=order_id, object_instance=order)
        return {"message": "Commande mise à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/order/{order_id}")
def delete_order(order_id: int):
    """
    route permettant de supprimer une commande

    :param order_id: l'identifiant de la commande à supprimer
    """
    try:
        data_instance.order_CRUD("DELETE", object_id=order_id)
        return {"message": "Commande supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))

@router.options("/order")
async def options_root():
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)

@router.options("/order/{id}")
async def options_root(id: int):
    allowed_methods = ["GET","PUT","DELETE", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
