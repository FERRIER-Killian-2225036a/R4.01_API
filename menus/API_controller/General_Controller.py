"""
General Controller Module
=========================

This module contains the General_Controller class responsible for routing to the API of the application.

Attributes:
    app (FastAPI): The FastAPI application instance.
    data (Data): The data access instance.

"""

from fastapi import FastAPI
from API_controller.API import API_Menus, API_Utils
from data_access.Data import Data
from starlette.middleware.cors import CORSMiddleware
from core.config import API_CORS_ORIGINS
from fastapi.responses import JSONResponse


class General_Controller:
    """
    Class for routing to the application's API.

    Attributes:
        app (FastAPI): The FastAPI application instance.
        data (Data): The data access instance.

    """

    app = FastAPI()

    def __init__(self, data: Data):
        """
        Constructor.

        Args:
            data (Data): The data access instance.

        """
        # Add CORS middleware to allow cross-origin requests
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=API_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.data = data

    @classmethod
    def setup_routes(cls):
        """
        Setup routes for API endpoints.

        """
        # Setup routes for API_Menus and API_Utils
        API_Menus.setup_routes(cls.app)
        print(" - Routes for API_Menus configured.")
        API_Utils.setup_routes(cls.app)
        print(" - Routes for API_Utils configured.")

    def data_transmission(self):
        """
        Transmit data to the API.

        """
        # Transmit data to API_Menus and API_Utils
        API_Menus.data_transmission(self.data)
        print(" - Data transmitted to API_Menus.")
        API_Utils.data_transmission(self.data)
        print(" - Data transmitted to API_Utils.")

    def getApp(self):
        """
        Get the FastAPI application instance.

        Returns:
            FastAPI: The FastAPI application instance.

        """
        return self.app
