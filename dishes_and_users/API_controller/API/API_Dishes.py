from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from data_access.Data import Data
from model_types.Dish import Dish

router = APIRouter()
data_instance: Data | None = None


def setup_routes(app):
    """
    Set up routes for managing Dish objects.

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


@router.post("/Dish")
def create_dish(dish: Dish):
    """
    Endpoint to create a new Dish object.

    Args:
        dish (Dish): The Dish object to create.

    Returns:
        dict: A message indicating successful creation.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        data_instance.ORM("CREATE", "DISH", object_instance=dish)
        return {"message": "Dish created successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/Dish/{id}")
def get_dish(id: int):
    """
    Endpoint to retrieve a Dish object by ID.

    Args:
        id (int): The ID of the Dish object to retrieve.

    Returns:
        dict: A message indicating successful retrieval along with the Dish object.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        dish = data_instance.ORM("READ", "DISH", object_id=id)
        if dish is None:
            raise ValueError("Dish not found")
        return {"message": "Dish retrieved successfully", "dish": dish}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/Dish/{id}")
def update_dish(id: int, dish: Dish):
    """
    Endpoint to update a Dish object.

    Args:
        id (int): The ID of the Dish object to update.
        dish (Dish): The updated Dish object.

    Returns:
        dict: A message indicating successful update.

    Raises:
        HTTPException: If an error occurs during update.
    """
    try:
        data_instance.ORM("UPDATE", "DISH", object_id=id, object_instance=dish)
        return {"message": "Dish updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/Dish/{id}")
def delete_dish(id: int):
    """
    Endpoint to delete a Dish object.

    Args:
        id (int): The ID of the Dish object to delete.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If an error occurs during deletion.
    """
    try:
        data_instance.ORM("DELETE", "DISH", object_id=id)
        return {"message": "Dish deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/Dish/list/")
async def list_dish():
    """
    Endpoint to retrieve a list of all Dish objects.

    Returns:
        dict: A message indicating successful retrieval along with the list of Dish objects.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        list_dish = data_instance.ORM("LIST", Dish.__name__.upper())
        if list_dish is None or list_dish == []:
            raise ValueError("No dishes in the database")
        return {"message": "Dishes listed successfully", "dishes": list_dish}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.options("/Dish")
async def options_root():
    """
    Endpoint to provide OPTIONS method for Dish operations.

    Returns:
        JSONResponse: A JSON response with allowed methods and headers.
    """
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)


@router.options("/Dish/{id}")
async def options_root(id: int):
    """
    Endpoint to provide OPTIONS method for Dish operations by ID.

    Args:
        id (int): The ID of the Dish object.

    Returns:
        JSONResponse: A JSON response with allowed methods and headers.
    """
    allowed_methods = ["GET", "PUT", "DELETE", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
