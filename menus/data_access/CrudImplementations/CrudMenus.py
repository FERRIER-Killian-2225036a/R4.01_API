import requests

from core.config import DISHES_AND_USER_API_ADRESS
from data_access.CrudInterface import CrudInterface
from model_types.Dish import Dish
from model_types.Menu import Menu


class CrudMenus(CrudInterface):

    def create(self, object_instance: Menu):
        dish_of_menu = object_instance.dict()["dishes"]
        dishes_list = requests.get(DISHES_AND_USER_API_ADRESS + "/list/").json()["dishes"]

        if len(dishes_list) == 0:
            for dish in dish_of_menu:
                requests.post(DISHES_AND_USER_API_ADRESS,
                              json={"id": 0, "description": dish["description"], "price": dish["price"]})
        else:
            for dish in dish_of_menu:
                present_in_api = False
                for dish_api in dishes_list:
                    if dish["description"] == dish_api["description"] and dish["price"] == dish_api["price"]:
                        present_in_api = True
                        break
                if not present_in_api:
                    requests.post(DISHES_AND_USER_API_ADRESS,
                                  json={"id": 0, "description": dish["description"], "price": dish["price"]})

        sql = "INSERT INTO MENU (utilisateur_id, dishes, date_creation, date_modification) VALUES (?, ?, ?, ?);"
        self.data_access.execute(sql, (
            object_instance.utilisateur_id, str(object_instance.dict()["dishes"]), object_instance.date_creation,
            object_instance.date_modification))
        self.data_access.commit()

    def read(self, object_id: int):
        sql = "SELECT * FROM MENU WHERE ID = ?;"
        request_responseult = self.data_access.execute(sql, (object_id,))
        request_responseult = request_responseult.fetchone()
        if request_responseult:
            menu = Menu(id=request_responseult[0], utilisateur_id=request_responseult[1],
                        dishes=[Dish(description=str(el["description"]), price=float(el["price"])) for el in
                                eval(request_responseult[2])], date_creation=request_responseult[3],
                        date_modification=request_responseult[4])
            return menu
        else:
            return None

    def update(self, object_id: int, object_instance: Menu):
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "UPDATE MENU SET utilisateur_id = ?, dishes = ?, date_creation = ?, date_modification = ? WHERE ID = ?;"
        self.data_access.execute(sql, (
            object_instance.utilisateur_id, object_instance.dishes, object_instance.date_creation,
            object_instance.date_modification, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "DELETE FROM MENU WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()
