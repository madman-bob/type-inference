from type_inference.types import Type, FuncType, type_simplicity
from type_inference.substitution import type_occurs, TypeSubstitution

__all__ = ["hindley_milner_unification"]


def hindley_milner_unification(a: Type, b: Type) -> TypeSubstitution:
    substitutions = TypeSubstitution()
    equations = [(a, b)]

    while equations:
        s, t = equations.pop()

        if s == t:
            continue

        if not isinstance(s, FuncType):
            if not isinstance(t, FuncType):
                s, t = sorted([s, t], key=type_simplicity, reverse=True)

            if type_occurs(s, t):
                raise TypeError("Circular type")

            equations = [
                (x[t / s], y[t / s])
                for x, y in equations
            ]
            substitutions += t / s

            continue

        if isinstance(s, FuncType) and isinstance(t, FuncType):
            if len(s.arg_types) != len(t.arg_types):
                raise TypeError("Inconsistent argument lengths")

            equations.extend(zip(s.type_params, t.type_params))

            continue

    return substitutions
