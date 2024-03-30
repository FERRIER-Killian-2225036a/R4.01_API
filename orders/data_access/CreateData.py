"""
Classe permettant la gestion des données

"""

from data_access.Singleton import Singleton
from core.config import FICHIER_SAUVEGARDE
import sqlite3

from model_types.Order import Order


class CreateData(metaclass=Singleton):
    file_path: str
    data_access: sqlite3.Connection

    def __init__(self, file_path):
        file_path = FICHIER_SAUVEGARDE
        self.file_path = file_path
        self.data_access = sqlite3.connect(self.file_path)

        # Verification tables existent
        if not self.tables_exist() :
            self.create_tables()

    def tables_exist(self):
        """
        methode permettant de verifier si les tables existent

        """
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ORDER'")
        return cursor.fetchone() is None

    def create_tables(self):
        """
        methode permettant de créer les tables dans la BD

        """
        def prepare_creation_tables():
            """
            methode permettant de créer la gestion des clés étrangères

            """
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_order():
            """
            methode permettant de créer la table order

            """
            self.data_access.execute(
                """
                    CREATE TABLE Orders (
                        command_id INT PRIMARY KEY AUTOINCREMENT,
                        user_id INT,
                        localisation_id INT,
                        price DOUBLE,
                        date DATETIME,
                        FOREIGN KEY (localisation_id) REFERENCES Localisation(localisation_id)
                    );
                """
            )
        def create_table_menusOfOrder() :
            """
            methode permettant de créer la table menusOfOrder
            Représente la liste des menus contenu dans la commande

            """
            self.data_access.execute(
                """
                    CREATE TABLE MenusOfOrder (
                        command_id INT,
                        menu_id INT,
                        quantity INT,
                        FOREIGN KEY (command_id) REFERENCES Orders(command_id),
                        FOREIGN KEY (menu_id) REFERENCES Menu(menu_id),
                        UNIQUE (command_id, menu_id, quantity)
                    );
                """
            )
        def create_table_localisation():
            """
            methode permettant de créer la table localisation

            """
            self.data_access.execute(
                """
                    CREATE TABLE Localisation (
                        localisation_id INTEGER PRIMARY KEY,
                        address TEXT,
                        city VARCHAR(25),
                        postal_code VARCHAR(5)
                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_localisation()
            create_table_order()
            create_table_menusOfOrder()

        except Exception as e :
            raise ValueError("Erreur lors création table - " + str(e))


