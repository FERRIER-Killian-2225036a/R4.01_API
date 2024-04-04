from behave import given, when, then
from dishes_and_users.model_types.User import User


@when('We try to create a User')
def step_create_user(context):
    context.response = context.client.post("/User", json={"id": 1,
                                                          "login": "test",
                                                          "password": "test"})



@then('User is created in the database')
def step_user_created(context):
    assert "User created successfully" in context.response.json()["message"]


@when("We try to read a User")
def step_read_user(context):
    context.response = context.client.get("/User/1")


@then("User is retrieved from the database in the response")
def step_user_readed(context):
    assert "User retrieved successfully" in context.response.json()["message"]
    assert context.response.json()["user"]["login"] == "test"
    assert context.response.json()["user"]["password"] == "NOT YOUR BUSINESS"
    assert context.response.json()["user"]["id"] == 1


@given("A User exists in the database")
def step_user_exist(context):
    user = User(id=1, login="test", password="test")
    context.client.post("/User", json=user.dict())


@when("We try to update the User")
def step_update_user(context):
    context.response = context.client.put("/User/1", json={"id": 1,
                                                           "login": "zozo",
                                                           "password": "zuzu"})


@then("User information is updated in the database")
def step_user_updated(context):
    assert "User updated successfully" in context.response.json()["message"]
    context.response_temp = context.client.get("/User/1")
    assert context.response_temp.json()["user"]["login"] == "zozo"
    assert context.response_temp.json()["user"]["password"] == "NOT YOUR BUSINESS"


@when("We try to delete the User")
def step_delete_user(context):
    context.response = context.client.delete("/User/1")


@then("User is removed from the database")
def step_user_deleted(context):
    assert "User deleted successfully" in context.response.json()["message"]
    context.response_temp = context.client.get("/User/1")
    assert "User not found" in context.response_temp.json()["detail"]
    assert context.response_temp.status_code == 412


@when("We try to create a User that already exists")
def step_user_already_exist(context):
    context.response = context.client.post("/User", json={"id": 1,
                                                          "login": "test",
                                                          "password": "test"})


@then("User creation fails")
def step_impl(context):
    assert "UNIQUE constraint failed: USER.login" in context.response.json()["detail"]


@when("We try to read a non-existing User")
def step_impl(context):
    context.response = context.client.get("/User/2")


@then("User is not found in the database")
def step_impl(context):
    assert "User not found" in context.response.json()["detail"]


@when("We try to update a non-existing User")
def step_impl(context):
    context.response = context.client.put("/User/2", json={"id": 2,
                                                           "login": "zozo",
                                                           "password": "zuzu"})


@then("User update operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table USER" in context.response.json()["detail"]


@when("We try to delete a non-existing User")
def step_impl(context):
    context.response = context.client.delete("/User/2")


@then("User delete operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table USER" in context.response.json()["detail"]
