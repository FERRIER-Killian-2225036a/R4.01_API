"""
Data Access Module
==================

This module provides access to data storage and operations.

It includes classes and functions for interacting with the database, performing CRUD operations,
and managing authentication.

Imports:
    - sqlite3: Library for SQLite database operations.
    - Literal: Type hint for specifying literal values.
    - SAVE_FILE: Constant for the path to the SQLite database file.
    - AuthenticationManager: Class for managing user authentication.
    - CrudDishes: Class for CRUD operations on Dish objects.
    - CrudUsers: Class for CRUD operations on User objects.
    - Singleton: Metaclass for implementing the Singleton design pattern.
    - Dish: Class representing a dish object.
    - User: Class representing a user object.
"""


import sqlite3
from typing import Literal

from core.config import SAVE_FILE
from data_access.Authentication.AuthenticationManager import AuthenticationManager
from data_access.CrudImplementations.CrudDishes import CrudDishes
from data_access.CrudImplementations.CrudUsers import CrudUsers
from data_access.Singleton import Singleton
from model_types.Dish import Dish
from model_types.User import User


class Data(metaclass=Singleton):
    """
    Data Class
    ==========

    This class provides access to data storage and operations.

    Attributes:
        file_path (str): The path to the SQLite database file.
        data_access (sqlite3.Connection): Connection to the SQLite database.
        crud_dish (CrudDishes): CRUD operations for Dish objects.
        crud_user (CrudUsers): CRUD operations for User objects.
        authentication_manager (AuthenticationManager): Manages user authentication.

    Methods:
        tables_exist(): Checks if the necessary tables exist in the database.
        create_tables(): Creates necessary tables if they don't exist.
        ORM(): Object-Relational Mapping function for CRUD operations and authentication.

    """

    file_path: str
    data_access: sqlite3.Connection
    crud_dish: CrudDishes
    crud_user: CrudUsers
    authentication_manager: AuthenticationManager

    def __init__(self, file_path=SAVE_FILE):
        """
        Initializes the Data class.

        Args:
            file_path (str, optional): The path to the SQLite database file. Defaults to SAVE_FILE.
        """
        self.file_path = file_path

        self.data_access = sqlite3.connect('file:' + self.file_path, uri=True,
                                           detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

        self.crud_user = CrudUsers(self.data_access)
        self.crud_dish = CrudDishes(self.data_access)
        self.authentication_manager = AuthenticationManager(self.data_access)

        if not self.tables_exist():
            self.create_tables()

    def tables_exist(self) -> bool:
        """
        Checks if necessary tables exist in the database.

        Returns:
            bool: True if tables exist, False otherwise.
        """
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER'")
        return cursor.fetchone() is not None

    def create_tables(self) -> None:
        """
        Creates necessary tables if they don't exist.
        """
        def prepare_creation_tables():
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_user():
            self.data_access.execute(
                """
                    CREATE TABLE USER (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        login TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    );
                """
            )

        def create_table_dish():
            self.data_access.execute(
                """
                    CREATE TABLE DISH (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT UNIQUE NOT NULL,
                        price REAL NOT NULL
                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_user()
            create_table_dish()

        except Exception as e:
            raise ValueError("Error during table creation: " + str(e))

    def ORM(self, method: Literal["CREATE", "READ", "UPDATE", "DELETE", "AUTHENTICATE", "LIST"],
            object_type: Literal["DISH", "USER"] | None = None,
            object_instance: Dish | User | None = None,
            object_id: int | None = None,
            credentials: (str | None, str | None) = (None, None)) -> any:
        """
        Object-Relational Mapping function for CRUD operations and authentication.

        Args:
            method (Literal["CREATE", "READ", "UPDATE", "DELETE", "AUTHENTICATE", "LIST"]):
                CRUD operation or authentication method to perform.
            object_type (Literal["DISH", "USER"] | None, optional):
                Type of object to operate on (DISH or USER). Defaults to None.
            object_instance (Dish | User | None, optional):
                Instance of Dish or User for create/update operations. Defaults to None.
            object_id (int | None, optional):
                ID of the object for read/update/delete operations. Defaults to None.
            credentials ((str | None, str | None), optional):
                User login and password for authentication. Defaults to (None, None).

        Raises:
            ValueError: If incorrect parameters are provided.

        Returns:
            any: The result of the CRUD operation or authentication.
        """
        if object_type not in ("DISH", "USER", None):
            raise ValueError("Invalid object_type provided")
        elif object_type is None:
            if method not in ["AUTHENTICATE"]:
                raise ValueError("No object_type provided")
        else:
            crud_function = getattr(self, f"crud_{object_type.lower()}")

        match method:
            case 'CREATE':
                if object_instance is None:
                    raise ValueError("Invalid parameters for method 'CREATE'")
                return crud_function.create(object_instance)
            case 'READ':
                if object_id is None:
                    raise ValueError("No object_id provided for method 'READ'")
                return crud_function.read(object_id)
            case 'UPDATE':
                if object_id is None or object_instance is None:
                    raise ValueError("Invalid parameters for method 'UPDATE'")
                return crud_function.update(object_id, object_instance)
            case 'DELETE':
                if object_id is None:
                    raise ValueError("No object_id provided for method 'DELETE'")
                return crud_function.delete(object_id)
            case 'AUTHENTICATE':
                if credentials[0] and credentials[1] and isinstance(credentials[0], str) and isinstance(credentials[1], str):
                    return self.authentication_manager.Authenticate(credentials[0], credentials[1])
                else:
                    raise ValueError("Invalid credentials provided")
            case 'LIST':
                try:
                    return crud_function.list()
                except Exception as e:
                    raise ValueError("No tuples found in this table: " + str(e))
            case _:
                raise ValueError("Method not allowed")
