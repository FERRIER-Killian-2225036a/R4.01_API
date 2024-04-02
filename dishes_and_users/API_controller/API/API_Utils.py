from fastapi import APIRouter, Request, HTTPException
from data_access.Data import Data
from core.config import AUTHOR, VERSION
from model_types.Dish import Dish

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
    return {"message": "Welcome to the Users and Dishes API",
            "version": VERSION,
            "Creator": AUTHOR}


@router.post("/auth")
async def auth(request: Request):
    try:
        json = await request.json()
        login = json["login"]
        password = json["password"]
        resultat = data_instance.ORM("AUTHENTICATE", credentials=[login, password])
        if resultat is True:
            return {"message": "Good credentials"}

    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


