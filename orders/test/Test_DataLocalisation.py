"""
Fichier permettant de tester le CRUD sur la table localisation
"""

import unittest

from data_access.Data import Data
from model_types.Localisation import Localisation
from core.config import FICHIER_SAUVEGARDE


class Test_DataLocalisation(unittest.TestCase):
    data: Data

    @classmethod
    def setUpClass(cls):
        """
        Initialisation avant les tests
        """
        cls.data = Data(FICHIER_SAUVEGARDE)

    def test_create_localisation(self):
        """
        Test unitaire : Création tuple table Localisation
        """
        loc = Localisation(localisation_id=1, address='123 Rue Test', city='Testville', postal_code='12345')
        created_localisation = self.data.localisation_CRUD("CREATE", loc, loc.localisation_id)
        self.assertEqual(created_localisation, loc)

    def test_read_localisation(self):
        """
        Test unitaire : Lecture tuple table Localisation
        """
        loc = Localisation(localisation_id=1, address='123 Rue Test', city='Testville', postal_code='12345')
        self.data.localisation_CRUD("CREATE", loc, loc.localisation_id)
        read_localisation = self.data.localisation_CRUD("READ", None, loc.localisation_id)
        self.assertEqual(read_localisation, loc)

    def test_update_localisation(self):
        """
        Test unitaire : Mise à jour tuple table Localisation
        """
        loc = Localisation(localisation_id=1, address='123 Rue Test', city='Testville', postal_code='12345')
        self.data.localisation_CRUD("CREATE", loc, loc.localisation_id)
        loc.address = '456 Rue Test'
        updated_localisation = self.data.localisation_CRUD("UPDATE", loc, loc.localisation_id)
        self.assertEqual(updated_localisation, loc)

    def test_delete_localisation(self):
        """
        Test unitaire : Suppression tuple table Localisation
        """
        loc = Localisation(localisation_id=1, address='123 Rue Test', city='Testville', postal_code='12345')
        self.data.localisation_CRUD("CREATE", loc, loc.localisation_id)
        self.data.localisation_CRUD("DELETE", None, loc.localisation_id)
        with self.assertRaises(ValueError):
            self.data.localisation_CRUD("READ", None, loc.localisation_id)


if __name__ == '__main__':
    unittest.main()
