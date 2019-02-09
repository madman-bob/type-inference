from toolz import flip

from type_inference.types import Type, FuncType
from type_inference.substitution import type_occurs, TypeSubstitution

__all__ = []


def construct_function(self, other):
    """
    Use `a ** b` to mean FunctionType(a, b)
    """
    if isinstance(self, Type):
        self = (self,)

    if not isinstance(self, tuple) or not isinstance(other, Type):
        raise TypeError("Invalid FunctionType constructor")

    return FuncType(self, other)


def type_occurs_(self, other):
    """
    Use `x in e` to mean whether type variable x is free in expression e
    """
    if not isinstance(other, Type):
        raise TypeError("Can only check for Type occurrences in other Types")

    return type_occurs(other, self)


def type_substitution_construction(self, other):
    """
    Use `e / x` to be the substitution replacing type variable x with expression e
    """
    if not isinstance(other, Type):
        return NotImplemented

    return TypeSubstitution({other: self})


def type_substitution(self, item):
    """
    Use `t[s]` to the result of applying substitution s to type t
    """
    if isinstance(item, tuple):
        item = sum(item, TypeSubstitution())

    if not isinstance(item, TypeSubstitution):
        raise TypeError("Can only apply TypeSubstitutions to Types")

    return item.apply(self)


Type.__pow__ = construct_function
Type.__rpow__ = flip(construct_function)
Type.__contains__ = type_occurs_
Type.__truediv__ = type_substitution_construction
Type.__getitem__ = type_substitution
