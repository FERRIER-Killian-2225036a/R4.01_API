"""
CRUD Interface Module
=====================

This module defines the CRUD interface for data access operations.

Dependencies:
    - sqlite3: Standard SQLite3 database interface module.
    - typing: Support for type hints.

"""

import sqlite3
from typing import Literal


class CrudInterface:
    """
    Interface for CRUD operations on database tables.

    Attributes:
        data_access (sqlite3.Connection): Connection to the SQLite database.

    """

    data_access: sqlite3.Connection

    def __init__(self, data_access: sqlite3.Connection):
        """
        Initializes the CrudInterface class.

        Args:
            data_access (sqlite3.Connection): Connection to the SQLite database.

        """
        self.data_access = data_access

    def is_object_exist(self, object_id: int, table: Literal["MENU"]) -> bool:
        """
        Checks if an object with the given ID exists in the specified table.

        Args:
            object_id (int): The ID of the object to check.
            table (Literal["MENU"]): The table to check for object existence.

        Returns:
            bool: True if the object exists, False otherwise.

        Raises:
            ValueError: If the table name is not allowed.

        """
        if not (table in ["MENU"]):
            raise ValueError("Table must be either 'MENU'")
        return self.data_access.execute(f"SELECT * FROM {table} WHERE ID = ?;",
                                        (str(object_id),)).fetchone() is not None

    def create(self, object_instance: object):
        """
        Creates a new object in the database.

        Args:
            object_instance (object): The object instance to create.

        """
        pass

    def read(self, object_id: int):
        """
        Reads an object from the database.

        Args:
            object_id (int): The ID of the object to read.

        """
        pass

    def update(self, object_id: int, object_instance: object):
        """
        Updates an object in the database.

        Args:
            object_id (int): The ID of the object to update.
            object_instance (object): The updated object instance.

        """
        pass

    def delete(self, object_id: int):
        """
        Deletes an object from the database.

        Args:
            object_id (int): The ID of the object to delete.

        """
        pass
