from unittest import TestCase

from type_inference.types import Type, NamedType, AbstractType, FuncType


class TestTypes(TestCase):
    def test_types_distinct(self):
        a, b = Type(), Type()

        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertNotEqual(a, b)

    def test_named_type_equality(self):
        self.assertEqual(NamedType("a"), NamedType("a"))

    def test_named_type_distinctness(self):
        self.assertNotEqual(NamedType("a"), NamedType("b"))

    def test_named_type_repr(self):
        self.assertEqual("a", repr(NamedType("a")))

    def test_abstract_type_equality(self):
        self.assertEqual(AbstractType("a"), AbstractType("a"))

    def test_abstract_type_distinctness(self):
        self.assertNotEqual(AbstractType("a"), AbstractType("b"))

    def test_abstract_type_repr(self):
        self.assertEqual("a", repr(AbstractType("a")))

    def test_function_type_equality(self):
        a, b = Type(), Type()

        self.assertEqual(FuncType((a,), b), FuncType((a,), b))

    def test_function_type_distinctness(self):
        a, b, c = Type(), Type(), Type()

        self.assertNotEqual(FuncType((a,), b), FuncType((a,), c))
        self.assertNotEqual(FuncType((a,), b), FuncType((c,), b))

    def test_function_type_repr(self):
        self.assertEqual("(a,) -> b", repr(FuncType((NamedType("a"),), NamedType("b"))))
