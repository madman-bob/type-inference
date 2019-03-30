from unittest import TestCase

from type_inference.types import Type
from type_inference.substitution import TypeSubstitution
from type_inference.unification.hindley_milner import hindley_milner_unification

a, b, c = Type(), Type(), Type()


class TestUnification(TestCase):
    def test_hindley_milner_unification_basic(self):
        self.assertEqual(
            a / b,
            hindley_milner_unification(a, b)
        )

    def test_hindley_milner_unification_noop(self):
        self.assertEqual(
            TypeSubstitution(),
            hindley_milner_unification(a, a)
        )

    def test_hindley_milner_unification_function_arg_types(self):
        self.assertEqual(
            a / b,
            hindley_milner_unification(
                a ** c,
                b ** c
            )
        )

    def test_hindley_milner_unification_function_return_type(self):
        self.assertEqual(
            a / b,
            hindley_milner_unification(
                c ** a,
                c ** b
            )
        )

    def test_hindley_milner_unification_jagged(self):
        self.assertEqual(
            b ** c / a,
            hindley_milner_unification(
                a,
                b ** c
            )
        )

    def test_hindley_milner_unification_circular_type(self):
        with self.assertRaises(TypeError):
            hindley_milner_unification(
                a,
                a ** a
            )

    def test_hindley_milner_unification_inconsistent_argument_lengths(self):
        with self.assertRaises(TypeError):
            hindley_milner_unification(
                (a, a) ** b,
                (a, a, a) ** b
            )
