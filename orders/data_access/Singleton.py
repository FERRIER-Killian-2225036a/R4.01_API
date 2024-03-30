"""
Classe représentant un singleton

"""
class Singleton(type):
    """
    Classe implémentant le design pattern singleton pour la base de donnée notamment

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
