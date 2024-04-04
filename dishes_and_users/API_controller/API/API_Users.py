from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from data_access.Data import Data
from model_types.User import User

router = APIRouter()
data_instance: Data | None = None


def setup_routes(app):
    """
    Set up routes for managing User objects.

    Args:
        app: The FastAPI application instance.
    """
    app.include_router(router)


def data_transmission(data: Data):
    """
    Transmit the data context to the database.

    Args:
        data (Data): The data context to transmit.
    """
    global data_instance
    if data_instance is None:
        data_instance = data


@router.post("/User")
def create_user(user: User):
    """
    Endpoint to create a new User object.

    Args:
        user (User): The User object to create.

    Returns:
        dict: A message indicating successful creation.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        data_instance.ORM("CREATE", "USER", object_instance=user)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/User/{id}")
def get_user(id: int):
    """
    Endpoint to retrieve a User object by ID.

    Args:
        id (int): The ID of the User object to retrieve.

    Returns:
        dict: A message indicating successful retrieval along with the User object.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        user = data_instance.ORM("READ", "USER", object_id=id)
        if user is None:
            raise ValueError("User not found")
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/User/{id}")
def update_user(id: int, user: User):
    """
    Endpoint to update a User object.

    Args:
        id (int): The ID of the User object to update.
        user (User): The updated User object.

    Returns:
        dict: A message indicating successful update.

    Raises:
        HTTPException: If an error occurs during update.
    """
    try:
        data_instance.ORM("UPDATE", "USER", object_id=id, object_instance=user)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/User/{id}")
def delete_user(id: int):
    """
    Endpoint to delete a User object.

    Args:
        id (int): The ID of the User object to delete.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If an error occurs during deletion.
    """
    try:
        data_instance.ORM("DELETE", "USER", object_id=id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/User/list/")
async def list_user():
    """
    Endpoint to retrieve a list of all User objects.

    Returns:
        dict: A message indicating successful retrieval along with the list of User objects.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        list_users = data_instance.ORM("LIST", User.__name__.upper())
        if list_users is None or list_users == []:
            raise ValueError("No users in the database")
        return {"message": "Users listed successfully", "users": list_users}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.options("/User")
async def options_root():
    """
    Endpoint to provide OPTIONS method for User operations.

    Returns:
        JSONResponse: A JSON response with allowed methods and headers.
    """
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)


@router.options("/User/{id}")
async def options_root(id: int):
    """
    Endpoint to provide OPTIONS method for User operations by ID.

    Args:
        id (int): The ID of the User object.

    Returns:
        JSONResponse: A JSON response with allowed methods and headers.
    """
    allowed_methods = ["GET", "PUT", "DELETE", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
