from behave import *


@given("a user with a username and a password")
def step_impl(context):
    context.username = "test"
    context.password = "test"
    context.client.post("/User", json={"id": 0, "login": context.username, "password": context.password})


@when("the user tries to authenticate correctly")
def step_impl(context):
    context.response = context.client.post("/auth", json={"login": str(context.username), "password": str(context.password)})

@then("the api should return a good response")
def step_impl(context):
    assert context.response.json()["message"] == "Good credentials"

@when("the user tries to authenticate with bad credentials")
def step_impl(context):
    context.response = context.client.post("/auth", json={"login": context.username, "password": "wrong passwd"})

@then("the api should return a bad response")
def step_impl(context):
    assert context.response.json()["detail"] == "Bad user or password"