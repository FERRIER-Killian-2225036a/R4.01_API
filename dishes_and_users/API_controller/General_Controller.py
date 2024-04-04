from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from API_controller.API import API_Dishes, API_Users, API_Utils
from core.config import API_CORS_ORIGINS
from data_access.Data import Data


class General_Controller:
    """
    Class for routing to the application's API.

    Attributes:
        app (FastAPI): FastAPI instance for handling API requests.
        data (Data): Instance of the `Data` class for data access.
    """

    app = FastAPI(default_response_class=JSONResponse)
    data: Data

    def __init__(self, data: Data,test=False):
        """
        Constructor for the General_Controller class.

        Args:
            data (Data): Instance of the Data class.
        """
        if not test:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[API_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        self.data = data

    @classmethod
    def setup_routes(cls):
        """
        Method to set up routes for various API endpoints.
        """
        API_Dishes.setup_routes(cls.app)
        print(" - Routes de API_Dishes configurées.")
        API_Users.setup_routes(cls.app)
        print(" - Routes de API_Users configurées.")
        API_Utils.setup_routes(cls.app)
        print(" - Routes de Api_Utils configurées.")

    def data_transmission(self):
        """
        Method to transmit data to the API.
        """
        API_Dishes.data_transmission(self.data)
        print(" - Données transmises à API_Dishes.")
        API_Users.data_transmission(self.data)
        print(" - Données transmises à API_Users.")
        API_Utils.data_transmission(self.data)
        print(" - Données transmises à API_Utils.")

    def getApp(self):
        """
        Method to get the FastAPI instance.

        Returns:
            FastAPI: The FastAPI instance.
        """
        return self.app
