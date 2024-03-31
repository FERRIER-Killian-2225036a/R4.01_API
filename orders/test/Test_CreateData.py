"""
Fichier permettant de tester la création des données
"""
import os
import unittest
import sqlite3
from data_access.CreateData import CreateData

# BD de test
DATABASE_PATH = "test_database.db"

class TestCreateData(unittest.TestCase):
    def setUp(self):
        os.remove(DATABASE_PATH)
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.create_data = CreateData(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_create_tables(self):
        #Vérification tables créées (dans constructeur)
        self.assertTrue(self.create_data.tables_exist())

if __name__ == '__main__':
    unittest.main()