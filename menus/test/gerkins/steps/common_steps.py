import os
from behave import given, when, then
from menus.data_access.Data import Data
from menus.API_controller.General_Controller import General_Controller
from fastapi.testclient import TestClient


@given('API is running')
def step_run_api(context):
    # supprimer test.db si existe
    data = Data("/tmp/test.db")
    if os.path.exists("/tmp/test.db"):
        data.data_access.execute("DELETE FROM MENU; ")
        data.data_access.commit()
        data.data_access.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME IN ('MENU');")
        data.data_access.commit()

    controller = General_Controller(data)
    controller.setup_routes()
    controller.data_transmission()
    context.client = TestClient(controller.getApp())


@then('Status code is "{status_code}"')
def step_status_code(context, status_code):
    print(status_code, context.response.status_code)
    assert context.response.status_code == int(status_code)
