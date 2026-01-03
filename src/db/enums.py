from enum import Enum

class Gender(str, Enum):
    MALE = "MALE",
    FEMALE = "FEMALE"

class Service(str, Enum):
    LOGIN = "LOGIN",
    SIGNUP = "SIGNUP"
    RECOVERY = "RECOVERY"