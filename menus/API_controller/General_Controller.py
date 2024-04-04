from fastapi import FastAPI
from API_controller.API import API_Menus, API_Utils
from data_access.Data import Data
from starlette.middleware.cors import CORSMiddleware
from core.config import API_CORS_ORIGINS
from fastapi.responses import JSONResponse

class General_Controller:
    """
    classe pour transmettre le routage vers l'api de l'application

    """
    app = FastAPI()
    data: Data

    def __init__(self,data: Data):
        """
        constructeur

        :param data:
        """
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
        appel des routes d'api de chaque fichiers d'api

        :return:
        """
        API_Menus.setup_routes(cls.app)
        print(" - Routes de API_Menus configurées.")
        API_Utils.setup_routes(cls.app)
        print(" - Routes de Api_Utils configurées.")

    def data_transmission(self):
        """
        transmet les données pour l'api

        :return:
        """
        API_Menus.data_transmission(self.data)
        print(" - Données transmises à API_Menus.")
        API_Utils.data_transmission(self.data)
        print(" - Données transmises à API_Utils.")


    def getApp(self):
        return self.app
