import sqlite3
from typing import Literal


class CrudInterface:
    """
    CRUD Interface
    ==============

    This class provides an interface for CRUD operations on database objects.

    Attributes:
        data_access (sqlite3.Connection): Connection to the SQLite database.

    Methods:
        __init__(): Initializes the CrudInterface instance.
        is_object_exist(): Checks if an object with the given ID exists in the specified table.
        create(): Creates a new object in the database.
        read(): Retrieves an object from the database by ID.
        update(): Updates an object in the database.
        delete(): Deletes an object from the database.
        list(): Retrieves a list of all objects from the database.

    """

    data_access: sqlite3.Connection

    def __init__(self, data_access: sqlite3.Connection):
        """
        Initializes the CrudInterface instance.

        Args:
            data_access (sqlite3.Connection): Connection to the SQLite database.
        """
        self.data_access = data_access

    def is_object_exist(self, object_id: int, table: Literal["USER", "DISH"]) -> bool:
        """
        Checks if an object with the given ID exists in the specified table.

        Args:
            object_id (int): The ID of the object to check.
            table (Literal["USER", "DISH"]): The table to search for the object.

        Returns:
            bool: True if the object exists, False otherwise.
        """
        if not (table in ["USER", "DISH"]):
            raise ValueError("Table must be either 'USER' or 'DISH'")
        return self.data_access.execute(f"SELECT * FROM {table} WHERE ID = ?;",
                                        (str(object_id),)).fetchone() is not None

    def create(self, object_instance: object):
        """
        Creates a new object in the database.

        Args:
            object_instance (object): The object to create in the database.
        """
        pass

    def read(self, object_id: int):
        """
        Retrieves an object from the database by ID.

        Args:
            object_id (int): The ID of the object to retrieve from the database.
        """
        pass

    def update(self, object_id: int, object_instance: object):
        """
        Updates an object in the database.

        Args:
            object_id (int): The ID of the object to update.
            object_instance (object): The updated object.
        """
        pass

    def delete(self, object_id: int):
        """
        Deletes an object from the database.

        Args:
            object_id (int): The ID of the object to delete from the database.
        """
        pass

    def list(self):
        """
        Retrieves a list of all objects from the database.
        """
        pass
