from unittest import TestCase

from type_inference.types import Type, FuncType
from type_inference.substitution import TypeSubstitution

a, b, c, d = Type(), Type(), Type(), Type()


class TestNotation(TestCase):
    def test_function_construction(self):
        self.assertEqual(
            FuncType((a,), b),
            a ** b
        )

    def test_function_construction_multiple_arguments(self):
        self.assertEqual(
            FuncType((a, b), c),
            (a, b) ** c
        )

    def test_function_construction_associativity(self):
        self.assertEqual(
            FuncType((a,), FuncType((b,), c)),
            a ** b ** c
        )

    def test_function_construction_invalid(self):
        with self.subTest("Invalid first argument"), self.assertRaises(TypeError):
            1 ** a

        with self.subTest("Invalid return value"), self.assertRaises(TypeError):
            a ** 1

    def test_variable_contains_basic(self):
        self.assertTrue(a in a)

    def test_variable_contains_nested(self):
        with self.subTest("First argument"):
            self.assertTrue(a in a ** b)
            self.assertFalse(a in b ** c)

        with self.subTest("Second argument"):
            self.assertTrue(a in (b, a) ** c)
            self.assertFalse(a in (b, c) ** d)

        with self.subTest("Return value"):
            self.assertTrue(a in b ** a)
            self.assertFalse(a in b ** c)

        with self.subTest("Deeply nested"):
            self.assertTrue(a in (b ** a) ** c)
            self.assertFalse(a in (b ** c) ** d)

    def test_variable_contains_invalid(self):
        with self.assertRaises(TypeError):
            1 in a

    def test_type_substitution_construction(self):
        self.assertEqual(
            TypeSubstitution({b: a}),
            a / b
        )

    def test_type_substitution_replacement(self):
        self.assertEqual(
            a ** b,
            (c ** b)[a / c]
        )

    def test_type_substitution_multiple_replacement(self):
        self.assertEqual(
            a ** b,
            (c ** d)[a / c, b / d]
        )

    def test_type_substitution_invalid(self):
        with self.assertRaises(TypeError):
            a[1]
