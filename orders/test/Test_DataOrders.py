"""
Fichier permettant de tester le CRUD sur la table Order
"""

import unittest
from core.config import FICHIER_SAUVEGARDE
from model_types.Localisation import Localisation
from model_types.Order import Order
from data_access.Data import Data


class Test_DataOrders(unittest.TestCase):
    data: Data

    @classmethod
    def setUpClass(cls):
        """
        Initialisation avant les tests
        """
        cls.data = Data(FICHIER_SAUVEGARDE)

    def test_create_order(self):
        """
        Test unitaire : Création tuple table Order
        """
        loc = Localisation(localisation_id=1, address='a', city='Aix', postal_code=13100)
        order = Order(command_id=1, menus_id=[1, 2], user_id=1, localisation=loc, price=100.0,
                      date="2022-04-01")
        created_order = self.data.order_CRUD("CREATE", order)
        self.assertIsNotNone(created_order.command_id)

    def test_read_order(self):
        """
        Test unitaire : Lecture tuple table Order
        """
        localisation = Localisation(localisation_id=2, address="b", city="Marseille", postal_code=1300)
        order = Order(command_id=2, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.data.order_CRUD("CREATE", order)

        # Maintenant, lisez la commande et vérifiez si les attributs sont corrects
        read_order = self.data.order_CRUD("READ", None, created_order.command_id)
        self.assertEqual(created_order.menus_id, read_order.menus_id)
        self.assertEqual(created_order.user_id, read_order.user_id)
        self.assertEqual(created_order.price, read_order.price)
        self.assertEqual(created_order.date, read_order.date)

    def test_update_order(self):
        """
        Test unitaire : Mise à jour tuple table Order
        """
        localisation = Localisation(localisation_id=3, address="c", city="Menton", postal_code=6500)
        order = Order(command_id=3, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.data.order_CRUD("CREATE", order)
        updated_localisation = Localisation(localisation_id=2, address="b", city="Marseille", postal_code=1300)
        updated_order = Order(command_id=created_order.command_id, menus_id=[3, 4], user_id=2,
                              localisation=updated_localisation,
                              price=200.0, date="2022-04-02")
        self.data.order_CRUD("UPDATE", updated_order)
        read_order = self.data.order_CRUD("READ", None, created_order.command_id)
        self.assertEqual(updated_order.menus_id, read_order.menus_id)
        self.assertEqual(updated_order.user_id, read_order.user_id)
        self.assertEqual(updated_order.price, read_order.price)
        self.assertEqual(updated_order.date, read_order.date)

    def test_delete_order(self):
        """
        Test unitaire : Suppression tuple table Order
        """
        localisation = Localisation(localisation_id=4, address="d", city="Aix", postal_code=13100)
        order = Order(command_id=4, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.data.order_CRUD("CREATE", order)
        self.data.order_CRUD("DELETE", None, created_order.command_id)
        with self.assertRaises(ValueError):
            self.data.order_CRUD("READ", None, created_order.command_id)


if __name__ == '__main__':
    unittest.main()
