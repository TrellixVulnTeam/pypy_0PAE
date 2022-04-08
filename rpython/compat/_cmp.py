from ._types import ClassType


def cmp(a, b):
    if hasattr(a, "__cmp__") and not isinstance(a, (type, ClassType)):
        return a.__cmp__(b)

    if a == b:
        return 0
    if a < b:
        return -1
    return 1


def ordering_from_cmp(cls):
    if "__cmp__" not in cls.__dict__:
        return cls

    for key, derived in (
        ("__eq__", _derived_eq),
        ("__gt__", _derived_gt),
        ("__lt__", _derived_lt),
        ("__ge__", _derived_ge),
        ("__le__", _derived_le),
    ):
        if key not in cls.__dict__:
            setattr(cls, key, derived)

    return cls


def _derived_eq(self, other):
    return self.__cmp__(other) == 0


def _derived_gt(self, other):
    return self.__cmp__(other) == 1


def _derived_lt(self, other):
    return self.__cmp__(other) == -1


def _derived_ge(self, other):
    return self.__cmp__(other) in (0, 1)


def _derived_le(self, other):
    return self.__cmp__(other) in (0, -1)
