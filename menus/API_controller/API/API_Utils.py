from fastapi import APIRouter,Request
from menus.data_access.Data import Data
from menus.core.config import AUTHOR, VERSION

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
    return {"message": "Welcome to the Menus API",
            "version": VERSION,
            "Creator": AUTHOR}


