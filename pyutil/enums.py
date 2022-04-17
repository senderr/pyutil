from enum import Enum

class EnumBase(Enum):
    """Enum extension that adds convenience methods"""
    @classmethod
    def members(cls):
        return set(cls[c] for c in cls.__members__)

    @classmethod
    def names(cls):
        return set(cls[c].name for c in cls.__members__)

    def __lt__(self, other):
        """Used for sorting"""
        return self.name < other.name

class NameEnumMeta(type):
    def __len__(self):
        return self.__len__()

    def __init__(self, name, bases, dict):
        self.__reserved_fields__ = ["_names", "_values", "_reverse_lookup"]
        self.__fields__ = {}
        for k in dict.keys():
            if not k.startswith("__") and k not in self.__reserved_fields__:
                self.__fields__[k] = dict[k]


class NameEnum(str, metaclass=NameEnumMeta):
    """Base class for simple plain class string enums"""
    @classmethod
    def _names(cls):
        return list(cls.__fields__.keys())
    
    @classmethod
    def _values(cls):
        return list(cls.__fields__.values())
    
    @classmethod
    def _reverse_lookup(cls, value):
        for k, v in cls.__fields__.items():
            if v == value:
                return k
        raise ValueError(f"{value} not in {cls.__name__}")

    @classmethod
    def __len__(cls):
        return len(cls._names())