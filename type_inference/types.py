from dataclasses import dataclass, field
from itertools import count
from typing import Tuple

from ordering import Ordering

__all__ = ["Type", "NamedType", "AbstractType", "FuncType", "BOOL", "INT", "type_simplicity"]

# Type simplicity is an ordering on types, where types defined earlier are considered "simpler"
type_simplicity = Ordering()


@dataclass(eq=False, frozen=True)
class Type:
    def __post_init__(self):
        if self not in type_simplicity:
            type_simplicity.insert_end(self)


@dataclass(frozen=True)
class NamedType(Type):
    type_name: str = field(default_factory=lambda: "t{}".format(next(NamedType._counter)))

    _counter = count()

    def __repr__(self):
        return self.type_name


@dataclass(frozen=True)
class AbstractType(Type):
    type_name: str = field(default_factory=lambda: "a{}".format(next(NamedType._counter)))

    _counter = count()

    def __repr__(self):
        return self.type_name


@dataclass(frozen=True)
class FuncType(Type):
    arg_types: Tuple[Type, ...]
    return_type: Type

    def __post_init__(self):
        pass

    @property
    def type_params(self):
        return self.arg_types + (self.return_type,)

    def __repr__(self):
        return f"{self.arg_types!r} -> {self.return_type!r}"


BOOL = NamedType(type_name="bool")
INT = NamedType(type_name="int")
