"""
Menu API Module
===============

This module provides API routes for managing Menu entities.

Attributes:
    router (APIRouter): The APIRouter instance for defining routes.
    data_instance (Data | None): The instance of Data class for data access.

"""

from fastapi import APIRouter, HTTPException
from data_access.Data import Data
from model_types.Menu import Menu
from fastapi.responses import JSONResponse

# Initialize APIRouter instance
router = APIRouter()

# Initialize data_instance to None initially
data_instance: Data | None = None


def setup_routes(app):
    """
    Setup routes for Menu API.

    Args:
        app: The FastAPI application instance.

    """
    app.include_router(router)


def data_transmission(data: Data):
    """
    Transmit data instance to the API.

    Args:
        data (Data): The instance of Data class for data access.

    """
    global data_instance
    if data_instance is None:
        data_instance = data


@router.post("/Menu")
def create_menu(menu: Menu):
    """
    Route for creating a menu.

    Args:
        menu (Menu): The Menu instance to create.

    Returns:
        dict: JSON response indicating success or failure.

    Raises:
        HTTPException: If an error occurs during menu creation.

    """
    try:
        data_instance.ORM("CREATE", Menu.__name__.upper(), object_instance=menu)
        return {"message": "menu created with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.get("/Menu/{id}")
def get_menu(id: int):
    """
    Route for retrieving a menu by ID.

    Args:
        id (int): The ID of the menu to retrieve.

    Returns:
        dict: JSON response containing the retrieved menu.

    Raises:
        HTTPException: If the menu is not found.

    """
    try:
        menu = data_instance.ORM("READ", Menu.__name__.upper(), object_id=id)
        if menu is None:
            raise ValueError("Menu not found")
        return {"message": "menu readed with success", "menu": menu}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.put("/Menu/{id}")
def update_menu(id: int, menu: Menu):
    """
    Route for updating a menu.

    Args:
        id (int): The ID of the menu to update.
        menu (Menu): The updated Menu instance.

    Returns:
        dict: JSON response indicating success or failure.

    Raises:
        HTTPException: If an error occurs during menu update.

    """
    try:
        data_instance.ORM("UPDATE", Menu.__name__.upper(), object_id=id, object_instance=menu)
        return {"message": "menu updated with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.delete("/Menu/{id}")
def delete_menu(id: int):
    """
    Route for deleting a menu.

    Args:
        id (int): The ID of the menu to delete.

    Returns:
        dict: JSON response indicating success or failure.

    Raises:
        HTTPException: If an error occurs during menu deletion.

    """
    try:
        data_instance.ORM("DELETE", Menu.__name__.upper(), object_id=id)
        return {"message": "menu deleted with success"}
    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.options("/Menu")
async def options_root():
    """
    Route for handling OPTIONS request on root menu endpoint.

    Returns:
        JSONResponse: JSON response containing allowed methods.

    """
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)


@router.options("/Menu/{id}")
async def options_root(id: int):
    """
    Route for handling OPTIONS request on menu endpoint with ID.

    Args:
        id (int): The ID of the menu.

    Returns:
        JSONResponse: JSON response containing allowed methods.

    """
    allowed_methods = ["GET", "PUT", "DELETE", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
