from data_access.Singleton import Singleton
from core.config import FICHIER_SAUVEGARDE
import sqlite3

from model_types.Order import Order


class Data(metaclass=Singleton):
    file_path: str
    data_access: sqlite3.Connection

    def __init__(self, file_path=FICHIER_SAUVEGARDE):
        self.file_path = file_path
        self.data_access = sqlite3.connect(self.file_path)

        # Verification tables existent
        if not self.tables_exist() :
            self.create_tables()



    def tables_exist(self):
        cursor = self.data_access.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ORDER'")
        return cursor.fetchone() is not None

    def create_tables(self):
        def prepare_creation_tables():
            self.data_access.execute("PRAGMA foreign_keys = ON")

        def create_table_order():
            self.data_access.execute(
                """
                    CREATE TABLE ORDER (
                        
                    );
                """
            )

        def create_table_localisation():
            self.data_access.execute(
                """
                    CREATE TABLE LOCALISATION (

                    );
                """
            )

        try:
            prepare_creation_tables()
            create_table_order()
            create_table_localisation()

        except Exception as e :
            raise ValueError("Erreur lors création table" + str(e) )



    def order_CRUD(self, method:str, object=None | Order, object_id=None | int)->Order :
        def create_order(order:Order)->Order :
            sql = "INSERT INTO ORDER (menus_id, user_id, localisation_id, price, date) VALUES (?,?,?,?,?);"
            self.data_access.execute(sql, (order.menus_id, order.user_id, order.localisation.localisation_id,
                                           order.price, order.date))
            self.data_access.commit()

        def read_order():
            pass

        match method :
            case "CREATE":
                if object is None:
                    raise ValueError("Erreur lors création commande (objet null)")
                if isinstance(object, Order):
                    return create_order(object)
                else:
                    raise ValueError("Erreur : mauvais type fournis en paramètre")