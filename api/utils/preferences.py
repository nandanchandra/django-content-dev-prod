from enum import Enum

class Gender(Enum):
    
    MALE = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]