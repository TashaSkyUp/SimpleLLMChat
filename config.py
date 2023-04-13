import abc
import os
import openai


# Load environment variables from .env file



class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(abc.ABC, metaclass=Singleton):
    pass


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """
    api_key = os.environ.get('OPENAI_API_KEY')
    organization = os.environ.get('OPENAI_ORG')

    def __init__(self):
        """Initialize the Config class"""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.organization = os.environ.get('OPENAI_ORG')

