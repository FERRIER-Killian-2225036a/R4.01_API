import os
import unittest
from core.config import FICHIER_SAUVEGARDE
from model_types.Localisation import Localisation
from model_types.Order import Order
from data_access.Data import Data

# BD de test
DATABASE_PATH = "test_database.db"
localisation: Localisation

class Test_DataOrders(unittest.TestCase):

    def setUp(self):
        # Initialisation de la base de données de test
        self.create_data = Data(DATABASE_PATH)

    def tearDown(self):
        # Nettoyage
        self.create_data.data_access.close()
        # Supprimer la base de données de test
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)

    def test_create_order(self):
        loc = Localisation(localisation_id=1, address='a', city='Aix', postal_code=13100)
        order = Order(command_id=1, menus_id=[1, 2], user_id=1, localisation=loc, price=100.0,
                      date="2022-04-01")
        created_order = self.create_data.order_CRUD("CREATE", order)
        self.assertIsNotNone(created_order.command_id)

    def test_read_order(self):
        # Créez d'abord une commande pour tester la lecture
        localisation = Localisation(localisation_id=2, address="b", city="Marseille", postal_code=1300)
        order = Order(command_id=2, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.create_data.order_CRUD("CREATE", order)

        # Maintenant, lisez la commande et vérifiez si les attributs sont corrects
        read_order = self.create_data.order_CRUD("READ", None, created_order.command_id)
        self.assertEqual(created_order.menus_id, read_order.menus_id)
        self.assertEqual(created_order.user_id, read_order.user_id)
        self.assertEqual(created_order.price, read_order.price)
        self.assertEqual(created_order.date, read_order.date)

    def test_update_order(self):
        # Création commande
        localisation = Localisation(localisation_id=3, address="c", city="Menton", postal_code=6500)
        order = Order(command_id=3, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.create_data.order_CRUD("CREATE", order)

        # Modifiez la commande
        updated_localisation = Localisation(localisation_id=2, address="b", city="Marseille", postal_code=1300)
        updated_order = Order(command_id=created_order.command_id, menus_id=[3, 4], user_id=2,
                              localisation=updated_localisation,
                              price=200.0, date="2022-04-02")
        self.create_data.order_CRUD("UPDATE", updated_order)

        # Lisez à nouveau la commande et vérifiez si les attributs ont été mis à jour
        read_order = self.create_data.order_CRUD("READ", None, created_order.command_id)
        self.assertEqual(updated_order.menus_id, read_order.menus_id)
        self.assertEqual(updated_order.user_id, read_order.user_id)
        self.assertEqual(updated_order.price, read_order.price)
        self.assertEqual(updated_order.date, read_order.date)

    def test_delete_order(self):
        # Créez d'abord une commande pour tester la suppression
        localisation = Localisation(localisation_id=4, address="d", city="Aix", postal_code=13100)
        order = Order(command_id=4, menus_id=[1, 2], user_id=1, localisation=localisation, price=100.0,
                      date="2022-04-01")
        created_order = self.create_data.order_CRUD("CREATE", order)

        # Supprimez la commande
        self.create_data.order_CRUD("DELETE", None, created_order.command_id)

        # Essayez de lire la commande supprimée et vérifiez qu'elle n'existe pas
        with self.assertRaises(ValueError):
            self.create_data.order_CRUD("READ", None, created_order.command_id)


if __name__ == '__main__':
    unittest.main()
