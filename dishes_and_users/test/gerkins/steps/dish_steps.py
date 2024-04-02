from behave import given, when, then
from dishes_and_users.model_types.Dish import Dish



@when('We try to create a Dish')
def step_create_user(context):
    context.response = context.client.post("/Dish", json={"id": 1,
                                                          "description": "test",
                                                          "price": 10})


@then('Dish is created in the database')
def step_user_created(context):
    assert "dish created with success" in context.response.json()["message"]


@when("We try to read a Dish")
def step_read_user(context):
    context.response = context.client.get("/Dish/1")


@then("Dish is retrieved from the database in the response")
def step_user_readed(context):
    assert "dish readed with success" in context.response.json()["message"]
    assert context.response.json()["dish"]["description"] == "test"
    assert context.response.json()["dish"]["price"] == 10
    assert context.response.json()["dish"]["id"] == 1


@given("A Dish exists in the database")
def step_user_exist(context):
    dish = Dish(id=1, description="test", price=10)
    context.client.post("/Dish", json=dish.dict())


@when("We try to update the Dish")
def step_update_user(context):
    context.response = context.client.put("/Dish/1", json={"id": 1,
                                                           "description": "zozo",
                                                           "price": 10})


@then("Dish information is updated in the database")
def step_user_updated(context):
    assert "dish updated with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Dish/1")
    assert context.response_temp.json()["dish"]["description"] == "zozo"
    assert context.response_temp.json()["dish"]["price"] == 10


@when("We try to delete the Dish")
def step_delete_user(context):
    context.response = context.client.delete("/Dish/1")


@then("Dish is removed from the database")
def step_user_deleted(context):
    assert "dish deleted with success" in context.response.json()["message"]
    context.response_temp = context.client.get("/Dish/1")
    assert "Dish not found" in context.response_temp.json()["detail"]
    assert context.response_temp.status_code == 412


@when("We try to create a Dish that already exists")
def step_user_already_exist(context):
    context.response = context.client.post("/Dish", json={"id": 1,
                                                          "description": "test",
                                                          "price": "10"})


@then("Dish creation fails")
def step_impl(context):
    assert "UNIQUE constraint failed: DISH.description" in context.response.json()["detail"]


@when("We try to read a non-existing Dish")
def step_impl(context):
    context.response = context.client.get("/Dish/2")


@then("Dish is not found in the database")
def step_impl(context):
    assert "Dish not found" in context.response.json()["detail"]


@when("We try to update a non-existing Dish")
def step_impl(context):
    context.response = context.client.put("/Dish/2", json={"id": 2,
                                                           "description": "zozo",
                                                           "price": 10})


@then("Dish update operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table DISH" in context.response.json()["detail"]


@when("We try to delete a non-existing Dish")
def step_impl(context):
    context.response = context.client.delete("/Dish/2")


@then("Dish delete operation fails")
def step_impl(context):
    assert "This object_id doesn't appear in table DISH" in context.response.json()["detail"]
