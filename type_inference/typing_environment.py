from dataclasses import dataclass, field
from typing import Dict, Callable

from toolz import keyfilter, valmap

from type_inference.types import Type, NamedType, AbstractType, FuncType, BOOL, INT
from type_inference.substitution import TypeSubstitution
from type_inference.unification.trivial import trivial_unification

__all__ = ["TypingEnvironment"]


@dataclass
class TypingEnvironment:
    types: Dict[object, Type] = field(default_factory=dict)
    unification_func: Callable[[Type, Type], TypeSubstitution] = trivial_unification

    def __getitem__(self, item):
        if isinstance(item, bool):
            return BOOL

        if isinstance(item, int):
            return INT

        if item in self.types:
            return self.types[item]

        if isinstance(item, str):
            self[item] = NamedType()
            return self[item]

        if isinstance(item, tuple):
            func_type = self[item[0]]

            arg_types = tuple(self[term] for term in item[1:])
            return_type = NamedType()

            try:
                unification_substitution = self.unification_func(
                    func_type,
                    FuncType(arg_types, return_type)
                )
                self.apply_type_substitution(unification_substitution)
            except TypeError:
                raise TypeError("Inconsistent typing")

            return return_type[unification_substitution]

        raise TypeError("Cannot find type of {}".format(item.__class__.__name__))

    def __setitem__(self, key, value):
        if isinstance(value, (bool, int)):
            if self[key] != value:
                raise TypeError("Inconsistent typing")
            return

        if key in self.types:
            try:
                self.apply_type_substitution(
                    self.unification_func(self.types[key], value)
                )
            except TypeError:
                raise TypeError("Inconsistent typing")
            return

        if isinstance(key, str):
            self.types[key] = value
            return

        if isinstance(key, tuple):
            self[key[0]] = tuple(self[term] for term in key[1:]) ** value
            return

        raise TypeError("Cannot find type of {}".format(value.__class__.__name__))

    def apply_type_substitution(self, type_substitution: TypeSubstitution):
        concrete_substitution = TypeSubstitution(keyfilter(
            lambda key: not isinstance(key, AbstractType),
            type_substitution.mapping
        ))

        self.types = valmap(concrete_substitution.apply, self.types)
