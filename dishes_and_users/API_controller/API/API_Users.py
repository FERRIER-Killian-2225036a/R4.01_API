from fastapi import APIRouter
from data_access.Data import Data
from dishes_and_users.model_types.User import User

router = APIRouter()


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