"""
Data Access Module
==================

This module provides data access functionalities for the API.

Dependencies:
    - sqlite3: Standard SQLite3 database interface module.
    - data_access.CrudImplementations.CrudMenus: CRUD operations implementation for Menu model.
    - data_access.Singleton: Singleton metaclass for managing database connection.
    - core.config: Configuration settings.
    - model_types.Menu: Menu model.
    - typing: Support for type hints.

"""

import sqlite3
from data_access.CrudImplementations.CrudMenus import CrudMenus
from data_access.Singleton import Singleton
from core.config import SAVE_FILE
from model_types.Menu import Menu
from typing import Literal


class Data(metaclass=Singleton):
    """
    Singleton class for managing data access.

    This class handles database connection and provides methods for CRUD operations.

    Attributes:
        file_path (str): The file path for the SQLite database.
        data_access (sqlite3.Connection): Connection to the SQLite database.
        crud_menu (CrudMenus): CRUD operations implementation for Menu model.

    """

    file_path: str
    data_access: sqlite3.Connection
    crud_menu: CrudMenus

    def __init__(self, file_path=SAVE_FILE):
        """
        Initializes the Data class.

        Args:
            file_path (str): The file path for the SQLite database.

        """
        self.file_path = file_path
        self.data_access = sqlite3.connect('file:' + self.file_path, uri=True,
                                           detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

        self.crud_menu = CrudMenus(self.data_access)

        if not self.tables_exist():
            self.create_tables()

    def tables_exist(self):
        """
        Checks if tables exist in the database.

        Returns:
            bool: True if tables exist, False otherwise.

        """
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MENU'")
        return cursor.fetchone() is not None

    def create_tables(self):
        """
        Creates tables in the database if they do not exist.

        Raises:
            ValueError: If an error occurs during table creation.

        """
        def prepare_creation_tables():
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_menu():
            self.data_access.execute(
                """
                    CREATE TABLE MENU (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        utilisateur_id INTEGER UNIQUE NOT NULL,
                        dishes TEXT UNIQUE NOT NULL,
                        date_creation VARCHAR NOT NULL,
                        date_modification VARCHAR NOT NULL
                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_menu()

        except Exception as e:
            raise ValueError("Error during table creation: " + str(e))

    def ORM(self, method: Literal["CREATE", "READ", "UPDATE", "DELETE"],
            object_type: Literal["MENU"] | None = None,
            object_instance: Menu | None = None,
            object_id: int | None = None):
        """
        Executes CRUD operations based on method and object type.

        Args:
            method (Literal["CREATE", "READ", "UPDATE", "DELETE"]): The CRUD method to execute.
            object_type (Literal["MENU"] | None): The type of object to operate on.
            object_instance (Menu | None): The instance of the Menu model.
            object_id (int | None): The ID of the object.

        Returns:
            Depends on the CRUD operation:
                - For CREATE: The created object.
                - For READ: The retrieved object.
                - For UPDATE: The updated object.
                - For DELETE: None.

        Raises:
            ValueError: If method or object type is not allowed, or if parameters are missing or incorrect.

        """
        if object_type not in ("MENU", None):
            raise ValueError("Wrong type given")
        else:
            crud_function = getattr(self, f"crud_{object_type.lower()}")
        match method:
            case 'CREATE':
                if object_instance is None:
                    raise ValueError("Wrong object_instance parameters for method Create")
                return crud_function.create(object_instance)
            case 'READ':
                if object_id is None:
                    raise ValueError("No object_id parameters for method Read")
                return crud_function.read(object_id)
            case 'UPDATE':
                if object_id is None or object_instance is None:
                    raise ValueError("object_instance or/and object_id is wrong for method Update")
                return crud_function.update(object_id, object_instance)
            case 'DELETE':
                if object_id is None:
                    raise ValueError("No object_id parameters for method Delete")
                return crud_function.delete(object_id)
            case 'LIST':
                try:
                    return crud_function.list()
                except Exception as e:
                    raise ValueError("No tuples in this table" + str(e))
            case _:
                raise ValueError("Method not allowed")
