from typing import Any

class UserMeta(type):


    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class User(metaclass=UserMeta):
    def __init__(self, id, name, email,login,password):
        self.__name = name
        self.__id = id
        self.__login = login
        self.__email = email
        self.__password=password
    @property
    def name(self):
        return self.__name

    @name.setter
    def name (self, value):
        self.__name = value

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value
    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        self.__login=value
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password=value
    def get_public_information(self):
        return {'email':self.__email,'login':self.__login}
