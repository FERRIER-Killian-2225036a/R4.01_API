"""
Fichier contenant les classes de test du CRUD de la table MenusOfOrder
"""

import unittest

from core.config import FICHIER_SAUVEGARDE
from data_access.Data import Data
from model_types.Localisation import Localisation
from model_types.Order import Order


class Test_DataMenusOfOrder(unittest.TestCase):
    data = Data

    @classmethod
    def setUpClass(cls):
        """
        Initialisation avant les tests
        """
        cls.data = Data(FICHIER_SAUVEGARDE)

    @classmethod
    def tearDownClass(cls):
        """
        Nettoyage après les tests
        """
        cursor = cls.data.data_access.cursor()
        cursor.execute("DELETE FROM Localisation")
        cls.data.data_access.commit()
        cls.data.data_access.close()

    def test_create_menusOfOrder(self):
        """
        Test unitaire : Création tuple table MenusOfOrder
        """
        loc = Localisation(localisation_id=1, address='a', city='Aix', postal_code=13100)
        order = Order(command_id=1, menus_id=[1, 2], user_id=1, localisation=loc, price=100.0, date="2022-04-01")
        created_order = self.data.order_CRUD("CREATE", order)
        # Ajout d'un menu à la commande
        menu_data = (created_order.command_id, 3, 2)  # (command_id, menu_id, quantity)
        created_menusOfOrder_id = self.data.menusOfOrder_CRUD("CREATE", menu_data)
        self.assertIsNotNone(created_menusOfOrder_id)

    def test_read_menusOfOrder(self):
        """
        Test unitaire : Lecture tuple table MenusOfOrder
        """
        order_id = 1
        menus = self.data.menusOfOrder_CRUD("READ", None, order_id)
        self.assertIsInstance(menus, list)

    def test_delete_menusOfOrder(self):
        """
        Test unitaire : Suppression tuple table MenusOfOrder
        """
        order_id = 1
        deleted_menusOfOrder = self.data.menusOfOrder_CRUD("DELETE", None, order_id)
        self.assertIsNone(deleted_menusOfOrder)


if __name__ == '__main__':
    unittest.main()
