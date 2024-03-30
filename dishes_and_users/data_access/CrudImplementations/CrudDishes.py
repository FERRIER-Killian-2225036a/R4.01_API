from dishes_and_users.data_access.CrudInterface import CrudInterface
from dishes_and_users.model_types.Dish import Dish


class CrudDishes(CrudInterface):

    def create(self, object_instance: Dish):
        sql = "INSERT INTO DISH (login, password) VALUES (?, ?);"
        self.data_access.execute(sql, (object_instance.description,
                                       object_instance.price))
        self.data_access.commit()

    def read(self, object_id: int):
        sql = "SELECT * FROM DISH WHERE ID = ?;"
        result = self.data_access.execute(sql, (object_id,)).fetchone()
        if result:
            dish = Dish(id=result[0], description=result[1], price=result[2])
            return dish
        else:
            return None

    def update(self, object_id: int, object_instance: Dish):
        if not self.is_object_exist(object_id, "DISH"):
            raise ValueError("This object_id doesn't appear in table DISH")
        sql = "UPDATE DISH SET description = ?, price = ? WHERE ID = ?;"
        self.data_access.execute(sql, (object_instance.description, object_instance.price, object_id))
        self.data_access.commit()

    def delete(self, object_id: int):
        if not self.is_object_exist(object_id, "DISH"):
            raise ValueError("This object_id doesn't appear in table DISH")
        sql = "DELETE FROM DISH WHERE ID = ?;"
        self.data_access.execute(sql, (object_id,))
        self.data_access.commit()
