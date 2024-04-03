import os
from behave import given, when, then
from menus.data_access.Data import Data
from menus.model_types.Menu import Menu
from menus.API_controller.General_Controller import General_Controller
from fastapi.testclient import TestClient



@when('We try to create a Menu')
def step_create_user(context):
    #TODO changer les dishes
    context.response = context.client.post("/Menu", json={"id": 1,
                                                          "utilisateur_id": 1,
                                                          "dishes": "aaaaa",
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })
    print(context.response)

@then('Menu is created in the database')
def step_user_created(context):
    assert "menu created with success" in context.response.json()["message"]


@when("We try to read a Menu")
def step_read_user(context):
    context.response = context.client.get("/Menu/1")


@then("Menu is retrieved from the database in the response")
def step_user_readed(context):
    assert "menu readed with success" in context.response.json()["message"]
    assert context.response.json()["menu"]["utilisateur_id"] == 1
    assert context.response.json()["menu"]["dishes"] == "DISHES"#TODO
    assert context.response.json()["menu"]["date_creation"] == "03/03/2024"
    assert context.response.json()["menu"]["date_modification"] == "03/03/2024"
    assert context.response.json()["menu"]["id"] == 1


@given("A Menu exists in the database")
def step_user_exist(context):
    menu = Menu(id=1, utilisateur_id=1, dishes="aaaa"#TODO
              , date_creation="03/03/2024", date_modification="03/03/2024")
    context.client.post("/Menu", json=menu.dict())


@when("We try to update the Menu")
def step_update_user(context):
    context.response = context.client.put("/Menu/1", json={"id": 1,
                                                          "utilisateur_id": "1",
                                                          "dishes": "aaaaa", ##TODO
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })


@then("Menu information is updated in the database")
def step_user_updated(context):
    assert "menu updated with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Menu/1")
    assert context.response.json()["menu"]["utilisateur_id"] == 1
    assert context.response.json()["menu"]["dishes"] == "DISHES"#TODO
    assert context.response.json()["menu"]["date_creation"] == "03/03/2024"
    assert context.response.json()["menu"]["date_modification"] == "03/03/2024"


@when("We try to delete the Menu")
def step_delete_user(context):
    context.response = context.client.delete("/Menu/1")


@then("Menu is removed from the database")
def step_user_deleted(context):
    assert "menu deleted with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Menu/1")
    assert "Menu not found" in context.response_temp.json()["detail"]
    assert context.response_temp.status_code == 412


@when("We try to create a Menu that already exists")
def step_user_already_exist(context):
    context.response = context.client.post("/Menu", json={"id": 1,
                                                          "utilisateur_id": "1",
                                                          "dishes": "aaaaa", ##TODO
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })


@then("Menu creation fails")
def step_impl(context):
    assert "UNIQUE constraint failed: MENU.description" in context.response.json()["detail"]


@when("We try to read a non-existing Menu")
def step_impl(context):
    context.response = context.client.get("/Menu/2")


@then("Menu is not found in the database")
def step_impl(context):
    assert "Menu not found" in context.response.json()["detail"]


@when("We try to update a non-existing Menu")
def step_impl(context):
    context.response = context.client.put("/Menu/2", json={"id": 1,
                                                          "utilisateur_id": "1",
                                                          "dishes": "aaaaa", ##TODO
                                                          "date_creation": "03/03/2024",
                                                          "date_modification": "03/03/2024"
                                                          })


@then("Menu update operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table MENU" in context.response.json()["detail"]


@when("We try to delete a non-existing Menu")
def step_impl(context):
    context.response = context.client.delete("/Menu/2")


@then("Menu delete operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table MENU" in context.response.json()["detail"]
