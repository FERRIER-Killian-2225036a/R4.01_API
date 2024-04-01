from fastapi import APIRouter
from data_access.Data import Data
from dishes_and_users.model_types.User import User
from fastapi import HTTPException

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


@router.post("/User")
def create_user(user: User):
    try :
        data_instance.ORM("CREATE",User.__name__.upper(),object_instance=user)
        return {"message":"user created with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/User/{id}")
def get_user(id: int):
    try:
        user = data_instance.ORM("READ", User.__name__.upper(), object_id=id)
        if user is None:
            raise ValueError("User not found")
        return {"message": "user readed with success","user": user}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/User/{id}")
def update_user(id: int, user: User):
    try:
        data_instance.ORM("UPDATE", User.__name__.upper(),object_id=id ,object_instance=user)
        return {"message": "user updated with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/User/{id}")
def delete_user(id: int):
    try:
        data_instance.ORM("DELETE", User.__name__.upper(), object_id=id)
        return {"message": "user deleted with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))

