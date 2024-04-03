from data_access.CrudInterface import CrudInterface
from model_types.Dish import Dish


class CrudDishes(CrudInterface):

    def create(self, object_instance: Dish):
        sql = "INSERT INTO DISH (description, price) VALUES (?, ?);"
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

    def list(self):
        sql = "SELECT * FROM DISH ;"
        result = self.data_access.execute(sql).fetchall()
        list_dish = []
        if result is not None and result is not []:
            for el in result:
                list_dish.append(Dish(id=el[0], description=el[1], price=float(el[2])))

        return list_dish
