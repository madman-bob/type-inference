from type_inference.types import Type, FuncType, type_simplicity
from type_inference.substitution import TypeSubstitution

__all__ = ["trivial_unification"]


def trivial_unification(a: Type, b: Type) -> TypeSubstitution:
    if isinstance(a, FuncType) and isinstance(b, FuncType):
        return sum(
            (
                trivial_unification(x, y)
                for x, y in zip(a.type_params, b.type_params)
            ),
            TypeSubstitution()
        ).closure()

    if isinstance(a, FuncType) or isinstance(b, FuncType):
        raise TypeError("Cannot unify terms of different types")

    if a == b:
        return TypeSubstitution()

    a, b = sorted([a, b], key=type_simplicity, reverse=True)

    return b / a
