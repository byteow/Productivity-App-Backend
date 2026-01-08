from enum import Enum

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Service(str, Enum):
    LOGIN = "LOGIN"
    SIGNUP = "SIGNUP"
    RECOVERY = "RECOVERY"
    UPDATE = "UPDATE"

class SurveyStatus(str, Enum):
    GENERATING = "GENERATING"
    PENDING = "PENDING"
    COMPLTETED = "COMPLETED"

class TaskStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TaskPriority(str, Enum):
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH"