import sqlite3

from menus.data_access.CrudImplementations.CrudMenus import CrudMenus
from menus.data_access.Singleton import Singleton
from menus.core.config import SAVE_FILE
from menus.model_types.Menu import Menu
from menus.model_types.Dish import Dish
from typing import Literal


class Data(metaclass=Singleton):
    file_path: str
    data_access: sqlite3.Connection
    crud_menu: CrudMenus

    def __init__(self, file_path=SAVE_FILE):
        self.file_path = file_path

        self.data_access = sqlite3.connect('file:' + self.file_path, uri=True,
                                           detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

        self.crud_menu = CrudMenus(self.data_access)

        if not self.tables_exist():
            self.create_tables()

    def tables_exist(self):
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MENU'")
        return cursor.fetchone() is not None

    def create_tables(self):
        def prepare_creation_tables():
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_menu():
            self.data_access.execute(
                """
                    CREATE TABLE MENU (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        utilisateur_id INTEGER UNIQUE NOT NULL,
                        dishes TEXT UNIQUE NOT NULL,
                        date_creation DATE NOT NULL,
                        date_modification DATE NOT NULL
                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_menu()

        except Exception as e:
            raise ValueError("Erreur lors des créations de tables" + str(e))

    def ORM(self, method: Literal["CREATE", "READ", "UPDATE", "DELETE"],
            object_type: Literal["MENU"] | None = None,
            object_instance: Menu | None = None,
            object_id: int | None = None):

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
            case _:
                raise ValueError("Method not allowed")
