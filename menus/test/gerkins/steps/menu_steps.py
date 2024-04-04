"""
Behave Step Definitions Module
==============================

This module defines step definitions for Behave scenarios related to Menu operations.

"""

import os
from behave import given, when, then

from model_types.Menu import Menu


@when('We try to create a Menu')
def step_create_user(context):
    """
    Step definition for creating a Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.post("/Menu", json={"id": 1,
                                                          "utilisateur_id": 1,
                                                          "dishes": [{"description": "coq", "price": 2},
                                                                     {"description": "chat", "price": 4}],
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })

@then('Menu is created in the database')
def step_user_created(context):
    """
    Step definition for verifying that a Menu is created.

    Args:
        context: The Behave context object.

    """
    assert "menu created with success" in context.response.json()["message"]


@when("We try to read a Menu")
def step_read_user(context):
    """
    Step definition for reading a Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.get("/Menu/1")


@then("Menu is retrieved from the database in the response")
def step_user_readed(context):
    """
    Step definition for verifying that a Menu is retrieved successfully.

    Args:
        context: The Behave context object.

    """
    assert "menu readed with success" in context.response.json()["message"]
    assert context.response.json()["menu"]["utilisateur_id"] == 1
    assert context.response.json()["menu"]["dishes"] == [{"description": "chien", "price": 2}, {"description": "chat", "price": 4}]
    assert context.response.json()["menu"]["date_creation"] == "03/03/2024"
    assert context.response.json()["menu"]["date_modification"] == "03/03/2024"
    assert context.response.json()["menu"]["id"] == 1


@given("A Menu exists in the database")
def step_user_exist(context):
    """
    Step definition for setting up an existing Menu.

    Args:
        context: The Behave context object.

    """
    menu = Menu(id=1, utilisateur_id=1, dishes=[{"description": "chien", "price": 2}, {"description": "chat", "price": 4}],
                date_creation="03/03/2024", date_modification="03/03/2024")
    context.client.post("/Menu", json=menu.dict())


@when("We try to update the Menu")
def step_update_user(context):
    """
    Step definition for updating a Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.put("/Menu/1", json={"id": 1,
                                                           "utilisateur_id": "1",
                                                           "dishes": [{"description": "chien", "price": 2}, {"description": "chat", "price": 4}],
                                                           "date_creation": "03/03/2024",
                                                           "date_modification": "03/03/2024"
                                                           })


@then("Menu information is updated in the database")
def step_user_updated(context):
    """
    Step definition for verifying that Menu information is updated.

    Args:
        context: The Behave context object.

    """
    assert "menu updated with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Menu/1")
    assert context.response.json()["menu"]["utilisateur_id"] == 1
    assert context.response.json()["menu"]["dishes"] == [{"description": "chien", "price": 2}, {"description": "chat", "price": 4}]
    assert context.response.json()["menu"]["date_creation"] == "03/03/2024"
    assert context.response.json()["menu"]["date_modification"] == "03/03/2024"


@when("We try to delete the Menu")
def step_delete_user(context):
    """
    Step definition for deleting a Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.delete("/Menu/1")


@then("Menu is removed from the database")
def step_user_deleted(context):
    """
    Step definition for verifying that a Menu is deleted.

    Args:
        context: The Behave context object.

    """
    assert "menu deleted with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Menu/1")
    assert "Menu not found" in context.response_temp.json()["detail"]
    assert context.response_temp.status_code == 412


@when("We try to create a Menu that already exists")
def step_user_already_exist(context):
    """
    Step definition for trying to create a Menu that already exists.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.post("/Menu", json={"id": 1,
                                                          "utilisateur_id": "1",
                                                          "dishes": [{"description": "chien", "price": 2}, {"description": "chat", "price": 4}],
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })


@then("Menu creation fails")
def step_impl(context):
    """
    Step definition for verifying that Menu creation fails due to existing menu.

    Args:
        context: The Behave context object.

    """
    assert "UNIQUE constraint failed: MENU.description" in context.response.json()["detail"]


@when("We try to read a non-existing Menu")
def step_impl(context):
    """
    Step definition for trying to read a non-existing Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.get("/Menu/2")


@then("Menu is not found in the database")
def step_impl(context):
    """
    Step definition for verifying that a Menu is not found in the database.

    Args:
        context: The Behave context object.

    """
    assert "Menu not found" in context.response.json()["detail"]


@when("We try to update a non-existing Menu")
def step_impl(context):
    """
    Step definition for trying to update a non-existing Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.put("/Menu/2", json={"id": 1,
                                                           "utilisateur_id": "1",
                                                           "dishes": [{"description": "chien", "price": 2}, {"description": "chat", "price": 4}],
                                                           "date_creation": "03/03/2024",
                                                           "date_modification": "03/03/2024"
                                                           })


@then("Menu update operation fails")
def step_impl(context):
    """
    Step definition for verifying that Menu update operation fails due to non-existing Menu.

    Args:
        context: The Behave context object.

    """
    assert "This object_id doesn't appear in table MENU" in context.response.json()["detail"]


@when("We try to delete a non-existing Menu")
def step_impl(context):
    """
    Step definition for trying to delete a non-existing Menu.

    Args:
        context: The Behave context object.

    """
    context.response = context.client.delete("/Menu/2")


@then("Menu delete operation fails")
def step_impl(context):
    """
    Step definition for verifying that Menu delete operation fails due to non-existing Menu.

    Args:
        context: The Behave context object.

    """
    assert "This object_id doesn't appear in table MENU" in context.response.json()["detail"]
