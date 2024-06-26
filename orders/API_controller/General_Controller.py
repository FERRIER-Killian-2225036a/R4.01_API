"""
Fichier représentant le controlleur principal de l'API Order

"""

from fastapi import FastAPI
from API_controller.API import API_Orders
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
        API_Orders.setup_routes(cls.app)
        print(" - Routes de API_Orders configurées.")

    def data_transmission(self):
        """
        transmet les données pour l'api

        :return:
        """
        API_Orders.data_transmission(self.data)
        print(" - Données transmises à API_Orders")



    def getApp(self):
        return self.app
