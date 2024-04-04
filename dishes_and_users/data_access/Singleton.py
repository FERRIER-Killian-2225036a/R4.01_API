class Singleton(type):
    """
    Singleton Metaclass
    ===================

    This metaclass implements the Singleton design pattern.

    Usage:
        class YourClass(metaclass=Singleton):
            pass

    Attributes:
        _instances (dict): Dictionary to store instances of classes.

    Methods:
        __call__(): Method to create and return a single instance of the class.

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Create and return a single instance of the class.

        Args:
            cls (class): The class being instantiated.
            *args: Positional arguments for the class constructor.
            **kwargs: Keyword arguments for the class constructor.

        Returns:
            object: The single instance of the class.

        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
