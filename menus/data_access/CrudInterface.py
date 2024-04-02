import sqlite3
from typing import Literal


class CrudInterface:
    data_access: sqlite3.Connection

    def __init__(self, data_access: sqlite3.Connection):
        self.data_access = data_access

    def is_object_exist(self, object_id: int, table: Literal["MENU"]) -> bool:
        if not (table in ["MENU"]):
            raise ValueError("Table must be either 'MENU'")
        return self.data_access.execute(f"SELECT * FROM {table} WHERE ID = ?;",
                                        (str(object_id),)).fetchone() is not None

    def create(self, object_instance: object):
        pass

    def read(self, object_id: int):
        pass

    def update(self, object_id: int, object_instance: object):
        pass

    def delete(self, object_id: int):
        pass
