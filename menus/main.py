"""
Main Module
===========

This module serves as the entry point for running the API server.

Usage:
    Run this script to start the API server. It initializes the necessary components, sets up routes,
    and starts the server.

Attributes:
    HOST (str): The host address for the API server. Default is read from core.config.
    PORT (int): The port number for the API server. Default is read from core.config.

Dependencies:
    - uvicorn: ASGI server implementation.
    - core.config: Configuration settings including HOST and PORT.
    - API_controller.General_Controller: Controller handling API requests.
    - data_access.Data: Data access module.

.. WARNING::

   Changing the HOST and PORT requires modifying the core.config file imported in this script.

"""

import uvicorn
from core.config import HOST, PORT
from API_controller.General_Controller import General_Controller
from data_access.Data import Data

if __name__ == "__main__":
    # Initialize data access
    data = Data()

    # Initialize the controller with data access
    controller = General_Controller(data)

    # Set up API routes
    controller.setup_routes()

    # Perform data transmission (if needed)
    controller.data_transmission()

    # Run the API server
    uvicorn.run(controller.getApp(), host=HOST, port=PORT)
