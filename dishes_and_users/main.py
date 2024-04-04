"""
Main Script
===========

This script initializes and runs the API server using Uvicorn.

.. note::
    Configuration variables such as `HOST` and `PORT` can be modified in the `config` file.

.. code-block:: bash

    python main.py

Import Statements
-----------------

.. code-block:: python

    import uvicorn
    from core.config import HOST, PORT
    from API_controller.General_Controller import General_Controller
    from data_access.Data import Data

Execution Control
-----------------

The script execution starts from this block.

.. code-block:: python

    if __name__ == "__main__":

Data Initialization
-------------------

An instance of the `Data` class is created to handle data access.

.. code-block:: python

    data = Data()

Controller Initialization
--------------------------

The `General_Controller` instance is created with the `Data` instance as its parameter.

.. code-block:: python

    controller = General_Controller(data)

Route Setup
-----------

Routes for the API are set up using the `setup_routes()` method of the `General_Controller` instance.

.. code-block:: python

    controller.setup_routes()

Data Transmission
-----------------

The data transmission process is initiated using the `data_transmission()` method of the `General_Controller` instance.

.. code-block:: python

    controller.data_transmission()

Server Execution
----------------

Finally, the Uvicorn server is run with the configured host and port.

.. code-block:: python

    uvicorn.run(controller.getApp(), host=HOST, port=PORT)
"""


import uvicorn
from core.config import HOST, PORT
from API_controller.General_Controller import General_Controller
from data_access.Data import Data

if __name__ == "__main__":
    data = Data()
    controller = General_Controller(data)
    controller.setup_routes()
    controller.data_transmission()
    uvicorn.run(controller.getApp(), host=HOST, port=PORT)
