from dishes_and_users.data_access.CrudInterface import CrudInterface
from dishes_and_users.model_types.User import User


class CrudUsers(CrudInterface):

    def create(self, object_instance: User):
        print(object_instance)
        sql = "INSERT INTO USER (login, password) VALUES (?, ?);"
        self.data_access.execute(sql,(object_instance.login,
                                      object_instance.password))
        self.data_access.commit()

    def read(self, object_id: int):
        sql = "SELECT * FROM USER WHERE ID = ?;"
        result = self.data_access.execute(sql, (object_id,)).fetchone()
        if result:
            user = User(id=result[0], login=result[1], password="NOT YOUR BUSINESS")
            return user
        else:
            return None

    def update(self, object_id: int, object_instance: User):
        if not self.is_object_exist(object_id, "USER"):
            raise ValueError("This object_id doesn't appear in table USER")
        sql = "UPDATE USER SET login = ?, password = ? WHERE ID = ?;"
        self.data_access.execute(sql, (object_instance.login, object_instance.password, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        if not self.is_object_exist(object_id, "USER"):
            raise ValueError("This object_id doesn't appear in table USER")
        sql = "DELETE FROM USER WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()

