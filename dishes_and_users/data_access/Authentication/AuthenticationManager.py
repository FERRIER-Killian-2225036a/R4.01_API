import sqlite3


class AuthenticationManager:
    data_acess: sqlite3.Connection

    def __init__(self,data_access:sqlite3.Connection):
        self.data_access = data_access

    def Authenticate(self,login:str,password:str):
        sql = "SELECT id,login FROM USER WHERE login=? and password=?;"
        result = self.data_access.execute(sql,(login,password) ).fetchone()
        if result is None:
            raise ValueError("Bad user or password")
        return True

