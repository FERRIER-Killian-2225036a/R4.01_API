"""
Classe permettant la gestion des données

"""
import integer

from data_access.CreateData import CreateData
from data_access.Singleton import Singleton
from core.config import FICHIER_SAUVEGARDE
import sqlite3

from model_types.Localisation import Localisation
from model_types.Order import Order


class Data(metaclass=Singleton):
    file_path: str
    data_access: sqlite3.Connection
    createData: CreateData

    def __init__(self, file_path=FICHIER_SAUVEGARDE):
        self.file_path = file_path
        self.data_access = sqlite3.connect('file:' + self.file_path, uri=True,
                                           detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        self.createData = CreateData(self.data_access)

        # Verification tables existent
        if self.createData.tables_not_exist():
            self.createData.create_tables()

    def localisation_CRUD(self, method: str, object=None | Localisation, object_id=None | int) -> Localisation | None:
        """
        methodes du CRUD pour la table Localisation

        :return: La localisation en question

        """

        def create_localisation(localisation: Localisation, loc_id: int):
            """
            methodes permettant d'ajouter une localisation dans la table Localisation

            :param: localisation objet
            :param loc_id: Id de la localisation

            """
            sql = "INSERT INTO Localisation (localisation_id, address, city, postal_code) VALUES (?, ?, ?, ?);"
            self.data_access.execute(sql, (loc_id, localisation.address, localisation.city, localisation.postal_code))
            self.data_access.commit()
            return localisation

        def read_localisation(object_id: int) -> Localisation:
            """
            methodes permettant de lire une localisation dans la table Localisation

            :param: object_id L'id de la localisation à lire
            :return la localisation lu

            """
            sql = "SELECT address, city, postal_code FROM Localisation WHERE localisation_id = ?;"
            curs = self.data_access.cursor()
            curs.execute(sql, (object_id,))
            # Récupération des données de la localisation
            row = curs.fetchone()
            # Vérification si une ligne a été retournée
            if row is None:
                raise ValueError("La localisation avec l'ID", object_id, " n'existe pas")
            # Création de l'objet Localisation avec les données récupérées
            address, city, postal_code = row
            return Localisation(localisation_id=object_id, address=address, city=city, postal_code=postal_code)

        def update_localisation(object_id: int, localisation: Localisation):
            """
            methodes permettant de mettre à jour une localisation dans la table Localisation

            :param: object_id L'id de la localisation à modifier
            :param: localisation La localisation contenant les nouvelles informations

            """
            sql = "UPDATE Localisation SET address = ?, city = ?, postal_code = ? WHERE localisation_id = ?;"
            self.data_access.execute(sql,
                                     (localisation.address, localisation.city, localisation.postal_code, object_id))
            self.data_access.commit()
            return localisation

        def delete_localisation(object_id: int):
            """
            methodes permettant de supprimer une localisation dans la table Localisation

            :param: object_id L'id de la localisation à supprimer

            """
            sql = "DELETE FROM Localisation WHERE localisation_id = ?;"
            self.data_access.execute(sql, (object_id,))
            self.data_access.commit()
            return None

        match method:
            case "CREATE":
                if object is None:
                    raise ValueError("Erreur lors création localisation (objet null)")
                else:
                    return create_localisation(object, object_id)
            case "READ":
                if object_id is None:
                    raise ValueError("Erreur lors lecture localisation (id null)")
                else:
                    return read_localisation(object_id)
            case "UPDATE":
                if object is None:
                    raise ValueError("Erreur lors modification localisation (objet null)")
                if object_id is None:
                    raise ValueError("Erreur lors modification localisation (id null)")
                else:
                    return update_localisation(object_id, object)
            case "DELETE":
                if object_id is None:
                    raise ValueError("Erreur lors suppression localisation (id null)")
                else:
                    return delete_localisation(object_id)

    def menusOfOrder_CRUD(self, method: str, object=(int, int, int), object_id=None | int) -> int | list[int] | None:
        """
        methodes du CRUD pour la table MenusOfOrder

        :return: L'id de la commande en question

        """

        def create_menusOfOrder(tuple: (int, int, int)) -> int:
            """
            methodes permettant d'ajouter un menu dans la table menusOfOrder

            :param: Couple de trois entier (command_id, menu_id, quantity)
            :return: Un entier correspondant à l'id de la commande

            """
            sql = "INSERT INTO MenusOfOrder (command_id, menu_id, quantity) VALUES (?, ?, ?);"
            self.data_access.execute(sql, (tuple[0], tuple[1], tuple[2]))
            self.data_access.commit()
            return tuple[0]

        def read_menusOfOrder(object_id: int) -> list[int]:
            """
            methodes permettant de lire les menus d'une commande

            :param: Couple de trois entier (command_id, menu_id, quantity)
            :return: Liste d'identifiants de menu
            """
            sql = "SELECT menu_id FROM MenusOfOrder WHERE command_id = ?;"
            curs = self.data_access.cursor()
            # Exécution de la requête SQL avec l'ID de la commande
            curs.execute(sql, (object_id,))
            menu_ids = [row[0] for row in curs.fetchall()]
            return menu_ids

        def delete_menusOfOrder(object_id: int):
            """
            methodes permettant de supprimer les menus d'une commande

            :param: Un entier correspondant à l'id de la commande
            """
            sql = "DELETE FROM MenusOfOrder WHERE command_id = ?;"
            self.data_access.execute(sql, (object_id,))
            self.data_access.commit()
            return None

        match method:
            case "CREATE":
                if object is None:
                    raise ValueError("Erreur lors création menusOfOrder (objet null)")
                else:
                    return create_menusOfOrder(object)
            case "READ":
                if object_id is None:
                    raise ValueError("Erreur lors lecture menusOfOrder (id null)")
                else:
                    return read_menusOfOrder(object_id)
            case "DELETE":
                if object_id is None:
                    raise ValueError("Erreur lors suppression menusOfOrder (id null)")
                else:
                    return delete_menusOfOrder(object_id)

    def order_CRUD(self, method: str,
                   object_instance:None | Order =None,
                   object_id:int | None = None) -> Order:
        """
        methodes du CRUD pour la table Order

        """

        def create_order(order: Order) -> Order:
            """
            methodes permettant d'ajouter une commande dans la table Order

            """
            sql = "INSERT INTO Orders (user_id, localisation_id, price, date) VALUES (?,?,?,?);"
            curs = self.data_access.cursor()
            curs.execute(sql, (order.user_id, order.localisation.localisation_id,
                               order.price, order.date))
            # Récupération de l'ID de la commande insérée
            order_id = curs.lastrowid
            order.command_id = order_id
            # Creation localisation
            self.localisation_CRUD("CREATE", order.localisation, order_id)
            # Creation d'un tuple pour chaque valeur de menus_id
            for menu_id in order.menus_id:
                self.menusOfOrder_CRUD("CREATE", (order_id, menu_id, 1), None)
            self.data_access.commit()
            return order

        def read_order(object_id: int) -> Order:
            """
            methodes permettant de lire une commande dans la table Order

            """
            sql = "SELECT user_id, localisation_id, price, date FROM Orders WHERE command_id = ?;"
            order_read = self.data_access.execute(sql, (object_id,)).fetchone()
            if order_read is None:
                raise ValueError("Impossible de lire la commande n" + str(object_id))
            read_menus_id = self.menusOfOrder_CRUD("READ", None, object_id)
            read_localisation = self.localisation_CRUD("READ", None, object_id)
            read_loc_format = {
                "localisation_id": read_localisation.localisation_id,
                "address": read_localisation.address,
                "city": read_localisation.city,
                "postal_code": read_localisation.postal_code
            }
            return Order(command_id=object_id, menus_id=read_menus_id, user_id=order_read[0],
                         localisation=read_loc_format, price=order_read[2], date=order_read[3])

        def update_order(object_id: int, order: Order):
            """
            methodes permettant de mettre à jour une commande dans la table Order

            """
            sql = "UPDATE Orders SET user_id=?, localisation_id=?, price=?, date=? WHERE command_id=?;"
            self.localisation_CRUD("UPDATE", order.localisation, order.localisation.localisation_id)
            self.data_access.execute(sql, (order.user_id, order.localisation.localisation_id,
                                           order.price, order.date, object_id))
            self.data_access.commit()
            return order

        def delete_order(object_id: int):
            """
            methodes permettant de supprimer une commande dans la table Order

            """
            # Suppression menus
            self.menusOfOrder_CRUD("DELETE", None, object_id)
            # Suppression commande
            sql = "DELETE FROM Orders WHERE command_id = ?;"
            self.data_access.execute(sql, (object_id,))
            self.data_access.commit()
            # Suppression localisation
            self.localisation_CRUD("DELETE", None, object_id)
            return None

        match method:
            case "CREATE":
                if object_instance is None:
                    raise ValueError("Erreur lors création commande (objet null)")
                else:
                    return create_order(object_instance)
            case "READ":
                if object_id is None:
                    raise ValueError("Erreur lors lecture commande (id null)")
                else:
                    return read_order(object_id)
            case "UPDATE":
                if object_id is None:
                    raise ValueError("Erreur lors modification commande (id null)")
                if object_instance is None:
                    raise ValueError("Erreur lors modification commande (objet null)")
                else:
                    return update_order(object_id, object_instance)
            case "DELETE":
                if object_id is None:
                    raise ValueError("Erreur lors suppression commande (id null)")
                else:
                    return delete_order(object_id)
