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
    :return:
    """
    global data_instance
    if data_instance is None:
        data_instance = data


@router.get("/order/{order_id}")
def read_order(order_id:int):
    return {"message": "Welcome to the API"}


@router.post("/order")
def create_order(order:Order):
    return {""}

@router.put("/order/{order_id}")
def update_order(order_id:int, order:Order):
    pass

@router.delete("/order/{order_id}")
def delete_order(order_id:int):
    pass