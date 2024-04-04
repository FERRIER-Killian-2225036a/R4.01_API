"""
Behave Test Module
==================

This module contains Behave tests for the API.

Usage:
    These tests are intended to validate the behavior of the API endpoints.

Dependencies:
    - os: Operating system functionalities.
    - behave: BDD test framework.
    - data_access.Data: Data access module.
    - API_controller.General_Controller: Controller handling API requests.
    - fastapi.testclient: Test client for FastAPI applications.

"""

import os
from behave import given, then
from data_access.Data import Data
from API_controller.General_Controller import General_Controller
from fastapi.testclient import TestClient


@given('API is running')
def step_run_api(context):
    """
    Steps to set up API for testing.

    This step initializes the API for testing purposes by setting up necessary data and routes.

    Args:
        context: The context object provided by Behave.

    Returns:
        None

    """
    # Delete test.db if it exists
    data = Data("test.db")
    if os.path.exists("test.db"):
        data.data_access.execute("DELETE FROM MENU; ")
        data.data_access.commit()
        data.data_access.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME IN ('MENU');")
        data.data_access.commit()

    # Initialize the controller with test data
    controller = General_Controller(data)
    controller.setup_routes()
    controller.data_transmission()

    # Initialize test client
    context.client = TestClient(controller.getApp())


@then('Status code is "{status_code}"')
def step_status_code(context, status_code):
    """
    Step to validate response status code.

    This step checks if the received response status code matches the expected status code.

    Args:
        context: The context object provided by Behave.
        status_code (str): The expected status code as a string.

    Returns:
        None

    """
    assert context.response.status_code == int(status_code)
