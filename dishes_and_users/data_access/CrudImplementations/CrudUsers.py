from data_access.CrudInterface import CrudInterface
from model_types.User import User


class CrudUsers(CrudInterface):
    """
    CRUD Users
    ==========

    This class provides CRUD operations for User objects.

    Inherits From:
        CrudInterface

    Methods:
        create(): Creates a new User object in the database.
        read(): Retrieves a User object from the database by ID.
        update(): Updates a User object in the database.
        delete(): Deletes a User object from the database.
        list(): Retrieves a list of all User objects from the database.

    """

    def create(self, object_instance: User):
        """
        Creates a new User object in the database.

        Args:
            object_instance (User): The User object to create in the database.
        """
        print(object_instance)
        sql = "INSERT INTO USER (login, password) VALUES (?, ?);"
        self.data_access.execute(sql, (object_instance.login, object_instance.password))
        self.data_access.commit()

    def read(self, object_id: int) -> User:
        """
        Retrieves a User object from the database by ID.

        Args:
            object_id (int): The ID of the User object to retrieve from the database.

        Returns:
            User: The retrieved User object.
        """
        sql = "SELECT * FROM USER WHERE ID = ?;"
        result = self.data_access.execute(sql, (object_id,)).fetchone()
        if result:
            user = User(id=result[0], login=result[1], password="NOT YOUR BUSINESS")
            return user
        else:
            return None

    def update(self, object_id: int, object_instance: User):
        """
        Updates a User object in the database.

        Args:
            object_id (int): The ID of the User object to update.
            object_instance (User): The updated User object.
        """
        if not self.is_object_exist(object_id, "USER"):
            raise ValueError("This object_id doesn't appear in table USER")
        sql = "UPDATE USER SET login = ?, password = ? WHERE ID = ?;"
        self.data_access.execute(sql, (object_instance.login, object_instance.password, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        """
        Deletes a User object from the database.

        Args:
            object_id (int): The ID of the User object to delete from the database.
        """
        if not self.is_object_exist(object_id, "USER"):
            raise ValueError("This object_id doesn't appear in table USER")
        sql = "DELETE FROM USER WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()

    def list(self) -> list[User]:
        """
        Retrieves a list of all User objects from the database.

        Returns:
            list[User]: A list of User objects.
        """
        sql = "SELECT * FROM USER ;"
        result = self.data_access.execute(sql).fetchall()
        list_user = []
        if result is not None and result is not []:
            for el in result:
                list_user.append(User(id=int(el[0]), login=el[1], password="NOT YOUR BUSINESS"))

        return list_user
