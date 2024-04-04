"""
CRUD Menus Implementation Module
================================

This module implements CRUD operations for the Menu model.

Dependencies:
    - requests: HTTP library for making requests.
    - core.config: Configuration settings.
    - data_access.CrudInterface: Interface for CRUD operations.
    - model_types.Dish: Dish model.
    - model_types.Menu: Menu model.

"""

import requests
from core.config import DISHES_AND_USER_API_ADRESS
from data_access.CrudInterface import CrudInterface
from model_types.Dish import Dish
from model_types.Menu import Menu
import termcolor as tc


class CrudMenus(CrudInterface):
    """
    Implementation of CRUD operations for the Menu model.

    Inherits from CrudInterface.

    """

    def create(self, object_instance: Menu):
        """
        Creates a new menu in the database.

        Args:
            object_instance (Menu): The Menu instance to create.

        """
        # Get the list of dishes from the API
        dish_of_menu = object_instance.dict()["dishes"]
        try:

            dishes_list = requests.get(DISHES_AND_USER_API_ADRESS + "/list/").json()["dishes"]
            # If the list of dishes is empty, create dishes in the API
            if len(dishes_list) == 0:
                for dish in dish_of_menu:
                    requests.post(DISHES_AND_USER_API_ADRESS,
                                  json={"id": 0, "description": dish["description"], "price": dish["price"]})
            else:
                # Check if each dish in the menu exists in the API, create if not
                for dish in dish_of_menu:
                    present_in_api = False
                    for dish_api in dishes_list:
                        if dish["description"] == dish_api["description"] and dish["price"] == dish_api["price"]:
                            present_in_api = True
                            break
                    if not present_in_api:
                        requests.post(DISHES_AND_USER_API_ADRESS,
                                      json={"id": 0, "description": dish["description"], "price": dish["price"]})
        except Exception as e:
            print(tc.colored("Error when trying to access to Dishes_and_Users because it may be unreachable", "red"))
        finally:
            # Insert the menu into the database
            sql = "INSERT INTO MENU (utilisateur_id, dishes, date_creation, date_modification) VALUES (?, ?, ?, ?);"
            self.data_access.execute(sql, (
                object_instance.utilisateur_id, str(object_instance.dict()["dishes"]), object_instance.date_creation,
                object_instance.date_modification))
            self.data_access.commit()

    def read(self, object_id: int):
        """
        Reads a menu from the database.

        Args:
            object_id (int): The ID of the menu to read.

        Returns:
            Menu: The retrieved menu.

        """
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