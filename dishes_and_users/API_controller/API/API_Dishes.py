from fastapi import APIRouter, HTTPException

from data_access.Data import Data
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


@router.post("/Dish")
def create_user(dish: Dish):
    try:
        data_instance.ORM("CREATE", Dish.__name__.upper(), object_instance=dish)
        return {"message": "dish created with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/Dish/{id}")
def get_user(id: int):
    try:
        dish = data_instance.ORM("READ", Dish.__name__.upper(), object_id=id)
        if dish is None:
            raise ValueError("Dish not found")
        return {"message": "dish readed with success", "dish": dish}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/Dish/{id}")
def update_user(id: int, dish: Dish):
    try:
        data_instance.ORM("UPDATE", Dish.__name__.upper(), object_id=id, object_instance=dish)
        return {"message": "dish updated with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/Dish/{id}")
def delete_user(id: int):
    try:
        data_instance.ORM("DELETE", Dish.__name__.upper(), object_id=id)
        return {"message": "dish deleted with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))
