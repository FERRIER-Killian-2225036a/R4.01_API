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
        sql_tuples = self.data_access.execute(sql, (object_id,))
        sql_tuple = sql_tuples.fetchone()
        if sql_tuple:
            menu = Menu(id=sql_tuple[0], utilisateur_id=sql_tuple[1],
                        dishes=[Dish(description=str(el["description"]), price=float(el["price"])) for el in
                                eval(sql_tuple[2])], date_creation=sql_tuple[3],
                        date_modification=sql_tuple[4])
            return menu
        else:
            return None

    def update(self, object_id: int, object_instance: Menu):
        """
        Met à jour un Menu dans la base de données.

        Args:
            object_id (int): L'identifiant du Menu à mettre à jour.
            object_instance (Menu): L'instance Menu mise à jour.

        Raises:
            ValueError: Si l'object_id n'apparaît pas dans la table MENU.

        """
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "UPDATE MENU SET utilisateur_id = ?, dishes = ?, date_creation = ?, date_modification = ? WHERE ID = ?;"
        self.data_access.execute(sql, (
            object_instance.utilisateur_id, object_instance.dishes, object_instance.date_creation,
            object_instance.date_modification, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        """
        Supprime un Menu de la base de données.

        Args:
            object_id (int): L'identifiant du Menu à supprimer.

        Raises:
            ValueError: Si l'object_id n'apparaît pas dans la table MENU.

        """
        if not self.is_object_exist(object_id, "MENU"):
            raise ValueError("This object_id doesn't appear in table MENU")
        sql = "DELETE FROM MENU WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()

    def list(self):
        """
        Récupère la liste de tous les Menus dans la base de données.

        Returns:
            list[Menu]: Liste de tous les Menus dans la base de données.

        """
        sql = "SELECT * FROM MENU ;"
        result = self.data_access.execute(sql).fetchall()
        list_menu = []
        if result is not None and result is not []:
            for el in result:
                list_menu.append(Menu(id=el[0], utilisateur_id=el[1],
                                      dishes=[Dish(description=str(el["description"]), price=float(el["price"])) for el
                                              in
                                              eval(el[2])], date_creation=el[3],
                                      date_modification=el[4]))

        return list_menu
