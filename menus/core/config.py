"""
Configuration Module
====================

This module contains configuration settings for the API.

Attributes:
    HOST (str): The host address for the API server.
    PORT (int): The port number for the API server.
    SAVE_FILE (str): The file path for the SQLite database.
    AUTHOR (str): The author of the API.
    VERSION (float): The version number of the API.
    DISHES_AND_USER_API_ADRESS (str): The address of the endpoint for dishes and users API.
    API_CORS_ORIGINS (list[str]): List of allowed origins for Cross-Origin Resource Sharing (CORS).

"""

HOST = "Localhost"  # Host address for the API server
PORT = 8000  # Port number for the API server
SAVE_FILE = "Save.db"  # File path for the SQLite database
AUTHOR = "Killian FERRIER"  # Author of the API
VERSION = 0.1  # Version number of the API
DISHES_AND_USER_API_ADRESS = "http://127.0.0.1:8000/Dish"  # Address of the endpoint for dishes and users API
API_CORS_ORIGINS = ["http://127.0.0.1:8000"]  # List of allowed origins for CORS
