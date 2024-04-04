"""
Configuration Variables
-----------------------

These variables define configuration settings for the application.

- `HOST` (str): The host address.
- `PORT` (int): The port number.
- `SAVE_FILE` (str): The file path for saving data.
- `AUTHOR` (str): The author of the application.
- `VERSION` (float): The version number of the application.
- `API_CORS_ORIGINS` (list): A list of allowed CORS origins for the API.

"""

HOST = "Localhost"
PORT = 8000
SAVE_FILE = "Save.db"
AUTHOR = "Tom Carvajal"
VERSION = 0.1
API_CORS_ORIGINS = ["http://localhost", "https://localhost", "https://localhost:1234", "https://localhost:8000",
                    "https://localhost:5173", "http://localhost:5173"]
