import sqlite3

from data_access.Authentication.AuthenticationManager import AuthenticationManager
from data_access.CrudImplementations.CrudUsers import CrudUsers
from data_access.CrudImplementations.CrudDishes import CrudDishes
from dishes_and_users.data_access.Singleton import Singleton
from dishes_and_users.core.config import SAVE_FILE
from model_types.Dish import Dish
from model_types.User import User
from typing import Literal


class Data(metaclass=Singleton):
    file_path: str
    data_access: sqlite3.Connection
    crud_dish: CrudDishes
    crud_user: CrudUsers
    authentication_manager: AuthenticationManager

    def __init__(self, file_path=SAVE_FILE):
        self.file_path = file_path

        self.data_access = sqlite3.connect('file:' + self.file_path, uri=True,
                                           detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

        self.crud_user = CrudUsers(self.data_access)
        self.crud_dishes = CrudDishes(self.data_access)
        self.authentication_manager = AuthenticationManager(self.data_access)

        if not self.tables_exist():
            self.create_tables()

    def tables_exist(self):
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER'")
        return cursor.fetchone() is not None

    def create_tables(self):
        def prepare_creation_tables():
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_user():
            self.data_access.execute(
                """
                    CREATE TABLE USER (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        login TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
                """
            )

        def create_table_dish():
            self.data_access.execute(
                """
                    CREATE TABLE DISH (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        price REAL NOT NULL
                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_user()
            create_table_dish()

        except Exception as e:
            raise ValueError("Erreur lors des créations de tables" + str(e))

    def ORM(self, method: Literal["CREATE", "READ", "UPDATE", "DELETE", "AUTHENTICATE"],
            object_type: Literal["DISH", "USER"] | None = None,
            object_instance: Dish | User | None = None,
            object_id: int | None = None,
            credentials: (str | None, str | None) = (None, None)):

        if object_type not in ("DISH", "USER", None):
            raise ValueError("Wrong type given")
        elif object_type is None:
            if not method == "AUTHENTICATE":
                raise "no type was given"
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
            case 'AUTHENTICATE':
                if credentials[0] and credentials[1] and type(credentials[0]) is str and type(credentials[1]) is str:
                    return self.authentication_manager.Authenticate(credentials[0], credentials[1])
                else:
                    raise ValueError("Wrong parameters Types / values in credentials")
            case _:
                raise ValueError("Method not allowed")
