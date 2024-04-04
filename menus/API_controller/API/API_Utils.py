"""
API Utilities Module
====================

This module provides utility functions and routes for the API.

Attributes:
    router (APIRouter): The APIRouter instance for defining routes.
    data_instance (Data | None): The instance of Data class for data access.

"""

from fastapi import APIRouter
from data_access.Data import Data
from core.config import AUTHOR, VERSION
from fastapi.responses import JSONResponse

# Initialize APIRouter instance
router = APIRouter()

# Initialize data_instance to None initially
data_instance: Data | None = None


def setup_routes(app):
    """
    Setup routes for API utilities.

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


@router.get("/")
def read_root():
    """
    Route for root endpoint.

    Returns:
        dict: JSON response containing welcome message, version, and creator information.

    """
    return {"message": "Welcome to the Menus API",
            "version": VERSION,
            "Creator": AUTHOR}
