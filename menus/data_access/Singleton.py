"""
Singleton Metaclass Module
==========================

This module defines a Singleton metaclass used for implementing the singleton design pattern.

"""


class Singleton(type):
    """
    Metaclass implementing the singleton design pattern.

    This metaclass ensures that only one instance of a class is created.

    Attributes:
        _instances (dict): Dictionary storing instances of classes.

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Call method to create or retrieve the instance of the class.

        Args:
            cls: The class.

        Returns:
            Instance of the class.

        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
