from enum import Enum


# Forward Definition
class NameEnum:
    ...


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


class RemovedAttribute:
    def __get__(self, instance, owner):
        raise AttributeError


class NameEnumMeta(type):
    def __len__(self):
        return len(self._values())

    def __iter__(self):
        return self._values().__iter__()

    def __delattr__(self, __name: str) -> None:
        if hasattr(self, __name) and __name in self.__fields__:
            del self.__fields__[__name]
            setattr(self, __name, RemovedAttribute())
        else:
            super().__delattr__(__name)

    def __init__(self, name, bases, dict):
        if len(bases) > 0 and issubclass(bases[0], NameEnum) and bases[0].__name__ != "NameEnum":
            parent_fields = bases[0].__fields__
            for k, v in parent_fields.items():
                setattr(self, k, v)
        else:
            parent_fields = {}

        self.__reserved_fields__ = ["_names", "_values", "_reverse_lookup"]
        self.__fields__ = parent_fields
        for k in dict.keys():
            if not k.startswith("__") and k not in self.__reserved_fields__:
                self.__fields__[k] = dict[k]

        super().__init__(name, bases, dict)


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
