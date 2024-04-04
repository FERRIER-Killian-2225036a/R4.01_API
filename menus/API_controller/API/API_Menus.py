from fastapi import APIRouter, HTTPException

from data_access.Data import Data
from model_types.Menu import Menu

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


@router.post("/Menu")
def create_menu(menu: Menu):
    try:
        print("from api :" ,menu,"\n")

        data_instance.ORM("CREATE", Menu.__name__.upper(), object_instance=menu)
        return {"message": "menu created with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/Menu/{id}")
def get_menu(id: int):
    try:
        print("get bien appelé")
        menu = data_instance.ORM("READ", Menu.__name__.upper(), object_id=id)
        print(menu)
        if menu is None:
            raise ValueError("Menu not found")
        return {"message": "menu readed with success", "menu": menu}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/Menu/{id}")
def update_menu(id: int, menu: Menu):
    try:
        data_instance.ORM("UPDATE", Menu.__name__.upper(), object_id=id, object_instance=menu)
        return {"message": "menu updated with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/Menu/{id}")
def delete_menu(id: int):
    try:
        data_instance.ORM("DELETE", Menu.__name__.upper(), object_id=id)
        return {"message": "menu deleted with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))
