from fastapi import APIRouter

from data_access.CreateData import Data
from dishes_and_users.model_types.Dish import Dish

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


@router.get("/")
def read_root():
    return {"message": "Welcome to the API"}


@router.post("/")
def root(dish: Dish) -> Dish:
    return dish
