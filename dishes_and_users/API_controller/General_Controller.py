from fastapi import FastAPI
from API_controller.API import API_Dishes, API_Users, API_Utils
from data_access.Data import Data


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

        self.data = data

    @classmethod
    def setup_routes(cls):
        """
        appel des routes d'api de chaque fichiers d'api

        :return:
        """
        API_Dishes.setup_routes(cls.app)
        print(" - Routes de API_Dishes configurées.")
        API_Users.setup_routes(cls.app)
        print(" - Routes de API_Users configurées.")
        API_Utils.setup_routes(cls.app)
        print(" - Routes de Api_Utils configurées.")

    def data_transmission(self):
        """
        transmet les données pour l'api

        :return:
        """
        API_Dishes.data_transmission(self.data)
        print(" - Données transmises à API_Dishes.")
        API_Users.data_transmission(self.data)
        print(" - Données transmises à API_Users.")
        API_Utils.data_transmission(self.data)
        print(" - Données transmises à API_Utils.")


    def getApp(self):
        return self.app
