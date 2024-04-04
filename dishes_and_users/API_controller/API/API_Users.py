from fastapi import APIRouter, HTTPException
from data_access.Data import Data
from model_types.User import User
from fastapi.responses import JSONResponse

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
    try:
        data_instance.ORM("CREATE", User.__name__.upper(), object_instance=user)
        return {"message": "user created with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/User/{id}")
def get_user(id: int):
    try:
        user = data_instance.ORM("READ", User.__name__.upper(), object_id=id)
        if user is None:
            raise ValueError("User not found")
        return {"message": "user readed with success", "user": user}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/User/{id}")
def update_user(id: int, user: User):
    try:
        data_instance.ORM("UPDATE", User.__name__.upper(), object_id=id, object_instance=user)
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


@router.get("/User/list/")
async def list_user():
    try:
        list_users = data_instance.ORM("LIST", User.__name__.upper())
        if list is None or list is []:
            raise ValueError("no users in the database")
        return {"message": "users listed with success",
                "dishes": list_users}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.options("/User")
async def options_root():
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)


@router.options("/User/{id}")
async def options_root(id: int):
    allowed_methods = ["GET", "PUT", "DELETE", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
