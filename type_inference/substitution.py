from dataclasses import dataclass, field
from typing import Iterable, Mapping

from toolz import itemfilter, merge, valmap

from type_inference.types import Type, FuncType

__all__ = ["free_vars", "type_occurs", "TypeSubstitution"]


def free_vars(structure: Type) -> Iterable[Type]:
    """
    Yields the free variables in a given structure
    """
    if isinstance(structure, FuncType):
        for param in structure.type_params:
            yield from free_vars(param)
    else:
        yield structure


def type_occurs(variable: Type, structure: Type) -> bool:
    """
    Returns whether type variable appears in a given structure
    """
    if variable == structure:
        return True

    if isinstance(structure, FuncType):
        return any(type_occurs(variable, param) for param in structure.type_params)

    return False


@dataclass
class TypeSubstitution:
    mapping: Mapping[Type, Type] = field(default_factory=dict)

    def apply(self, term: Type) -> Type:
        if term in self.mapping:
            return self.mapping[term]

        if isinstance(term, FuncType):
            return FuncType(
                arg_types=tuple(self.apply(arg_type) for arg_type in term.arg_types),
                return_type=self.apply(term.return_type)
            )

        return term

    def __add__(self, other):
        """
        The sub of two substitutions is the result of applying one substitution, followed by the other
        """
        if not isinstance(other, TypeSubstitution):
            return NotImplemented

        return TypeSubstitution(
            itemfilter(
                lambda item: item[0] != item[1],
                merge(
                    other.mapping,
                    valmap(other.apply, self.mapping)
                )
            )
        )
