import sqlite3


class AuthenticationManager:
    """
    Authentication Manager
    ======================

    This class manages user authentication.

    Attributes:
        data_acess (sqlite3.Connection): Connection to the SQLite database.

    Methods:
        __init__(): Initializes the AuthenticationManager instance.
        Authenticate(): Authenticates a user based on login and password.

    """

    data_acess: sqlite3.Connection

    def __init__(self, data_access: sqlite3.Connection):
        """
        Initializes the AuthenticationManager instance.

        Args:
            data_access (sqlite3.Connection): Connection to the SQLite database.
        """
        self.data_access = data_access

    def Authenticate(self, login: str, password: str) -> bool:
        """
        Authenticates a user based on login and password.

        Args:
            login (str): The user's login.
            password (str): The user's password.

        Returns:
            bool: True if authentication succeeds, False otherwise.
        """
        sql = "SELECT id, login FROM USER WHERE login=? and password=?;"
        result = self.data_access.execute(sql, (login, password)).fetchone()
        if result is None:
            raise ValueError("Bad user or password")
        return True
