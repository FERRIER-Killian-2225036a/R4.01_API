"""
Fichier permettant de tester la création des données

"""
import unittest
from data_access.Data import Data
from core.config import FICHIER_SAUVEGARDE


class TestCreateData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Data(FICHIER_SAUVEGARDE)

    def test_create_tables(self):
        """
        Test unitaire : vérification que les tables sont créées
        """
        self.assertTrue(self.connection.createData.tables_exist())

    def test_table_localisation_exist(self):
        """
        Test unitaire : vérification que la table localisation existe
        """
        cursor = self.connection.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Localisation';")
        self.assertIsNotNone(cursor.fetchone())


if __name__ == '__main__':
    unittest.main()
