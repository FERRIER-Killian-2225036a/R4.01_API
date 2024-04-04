from data_access.CrudInterface import CrudInterface
from model_types.Dish import Dish


class CrudDishes(CrudInterface):
    """
    CRUD Dishes
    ===========

    This class provides CRUD operations for Dish objects.

    Inherits From:
        CrudInterface

    Methods:
        create(): Creates a new Dish object in the database.
        read(): Retrieves a Dish object from the database by ID.
        update(): Updates a Dish object in the database.
        delete(): Deletes a Dish object from the database.
        list(): Retrieves a list of all Dish objects from the database.

    """

    def create(self, object_instance: Dish):
        """
        Creates a new Dish object in the database.

        Args:
            object_instance (Dish): The Dish object to create in the database.
        """
        sql = "INSERT INTO DISH (description, price) VALUES (?, ?);"
        self.data_access.execute(sql, (object_instance.description, object_instance.price))
        self.data_access.commit()

    def read(self, object_id: int) -> Dish:
        """
        Retrieves a Dish object from the database by ID.

        Args:
            object_id (int): The ID of the Dish object to retrieve from the database.

        Returns:
            Dish: The retrieved Dish object.
        """
        sql = "SELECT * FROM DISH WHERE ID = ?;"
        result = self.data_access.execute(sql, (object_id,)).fetchone()
        if result:
            dish = Dish(id=result[0], description=result[1], price=result[2])
            return dish
        else:
            return None

    def update(self, object_id: int, object_instance: Dish):
        """
        Updates a Dish object in the database.

        Args:
            object_id (int): The ID of the Dish object to update.
            object_instance (Dish): The updated Dish object.
        """
        if not self.is_object_exist(object_id, "DISH"):
            raise ValueError("This object_id doesn't appear in table DISH")
        sql = "UPDATE DISH SET description = ?, price = ? WHERE ID = ?;"
        self.data_access.execute(sql, (object_instance.description, object_instance.price, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        """
        Deletes a Dish object from the database.

        Args:
            object_id (int): The ID of the Dish object to delete from the database.
        """
        if not self.is_object_exist(object_id, "DISH"):
            raise ValueError("This object_id doesn't appear in table DISH")
        sql = "DELETE FROM DISH WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()

    def list(self) -> list[Dish]:
        """
        Retrieves a list of all Dish objects from the database.

        Returns:
            list[Dish]: A list of Dish objects.
        """
        sql = "SELECT * FROM DISH ;"
        result = self.data_access.execute(sql).fetchall()
        list_dish = []
        if result is not None and result is not []:
            for el in result:
                list_dish.append(Dish(id=el[0], description=el[1], price=float(el[2])))

        return list_dish
