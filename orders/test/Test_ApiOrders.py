"""
Fichier contenant les classes de test de l'API (routes)
"""

import unittest
from fastapi.testclient import TestClient

from core.config import FICHIER_SAUVEGARDE
from data_access.Data import Data
from model_types.Localisation import Localisation


class TestOrderRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initialisation avant les tests
        """
        cls.client = TestClient()
        cls.data = Data(FICHIER_SAUVEGARDE)
        cls.data_transmission(cls.data)

    def test_welcome_route(self):
        """
        Test unitaire : test route vide (de bienvenue)
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Bienvenue sur l'API"})

    def test_create_order_route(self):
        """
        Test unitaire : test route création commande
        """
        loc = Localisation(localisation_id=10, address="123 Rue de Test", city="Testville",
                                    postal_code="12345")
        order_data = {
            "command_id": 1,
            "menus_id": [1, 2],
            "user_id": 1,
            "localisation": loc,
            "price": 100.0,
            "date": "2022-04-01"
        }
        response = self.client.post("/order", json=order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "La commande a été crée"})

    def test_read_order_route(self):
        """
        Test unitaire : test route lecture commande
        """
        response = self.client.get("/order/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("Commande", response.json())

    def test_update_order_route(self):
        """
        Test unitaire : test route mise à jour commande
        """
        updated_order_data = {
            "command_id": 1,
            "menus_id": [1, 2],
            "user_id": 1,
            "localisation": {
                "localisation_id": 1,
                "address": "456 Rue de Test",
                "city": "Testville",
                "postal_code": "54321"
            },
            "price": 150.0,
            "date": "2022-05-01"
        }
        response = self.client.put("/order/1", json=updated_order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Commande mise à jour avec succès"})

    def test_delete_order_route(self):
        """
        Test unitaire : test route suppression commande
        """
        response = self.client.delete("/order/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Commande supprimée avec succès"})


if __name__ == '__main__':
    unittest.main()
