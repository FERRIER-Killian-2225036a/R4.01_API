from data_access.CrudInterface import CrudInterface
from model_types.Dish import Dish
from model_types.Menu import Menu


class CrudMenus(CrudInterface):

    def create(self, object_instance: Menu):
        print("type:", str(object_instance.dishes))
        dishes_string = object_instance.dict()["dishes"]
        print(type(dishes_string),str(dishes_string))
        #todo verif type dishes -> a transformer de json vers str
        sql = "INSERT INTO MENU (utilisateur_id, dishes, date_creation, date_modification) VALUES (?, ?, ?, ?);"
        self.data_access.execute(sql, (object_instance.utilisateur_id,
                                       str(object_instance.dict()["dishes"]),
                                       object_instance.date_creation,
                                       object_instance.date_modification))
        self.data_access.commit()

    def read(self, object_id: int):
        sql = "SELECT * FROM MENU WHERE ID = ?;"
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        result = self.data_access.execute(sql, (object_id,))
        result = result.fetchone()
        if result:

            print(type(eval(result[2])[1]))
            menu = Menu(id=result[0], utilisateur_id=result[1],
                        dishes=[Dish(description=str(el["description"]),
                                     price=float(el["price"])) for el in eval(result[2])],
                        date_creation=result[2], date_modification=result[2])
            return menu
        else:
            return None

    def update(self, object_id: int, object_instance: Menu):
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "UPDATE MENU SET utilisateur_id = ?, dishes = ?, date_creation = ?, date_modification = ? WHERE ID = ?;"
        self.data_access.execute(sql, (object_instance.utilisateur_id, object_instance.dishes,
                                       object_instance.date_creation, object_instance.date_modification, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "DELETE FROM MENU WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()
