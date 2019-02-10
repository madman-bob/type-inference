from unittest import TestCase

from type_inference.types import Type
from type_inference.substitution import TypeSubstitution
from type_inference.unification.trivial import trivial_unification

a, b, c = Type(), Type(), Type()


class TestTrivialUnification(TestCase):
    def test_trivial_unification(self):
        self.assertEqual(
            a / b,
            trivial_unification(a, b)
        )

    def test_trivial_unification_nop(self):
        self.assertEqual(
            TypeSubstitution(),
            trivial_unification(a, a)
        )

    def test_trivial_unification_nested(self):
        with self.subTest("First argument"):
            self.assertEqual(
                a / b,
                trivial_unification(a ** a, b ** a)
            )

        with self.subTest("Second argument"):
            self.assertEqual(
                a / b,
                trivial_unification((a, a) ** a, (a, b) ** a)
            )

        with self.subTest("Return value"):
            self.assertEqual(
                a / b,
                trivial_unification(a ** a, a ** b)
            )

        with self.subTest("Deeply nested"):
            self.assertEqual(
                a / b,
                trivial_unification((a ** a) ** a, (a ** b) ** a)
            )

    def test_trivial_unification_multiple_replacements(self):
        self.assertEqual(
            a / b + a / c,
            trivial_unification(a ** a, b ** c)
        )
        self.assertEqual(
            a / b + a / c,
            trivial_unification(a ** c, b ** a)
        )

    def test_trivial_unification_incompatible(self):
        with self.assertRaises(TypeError):
            trivial_unification(a, b ** c)
