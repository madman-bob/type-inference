from unittest import TestCase

from type_inference.types import Type, FuncType
from type_inference.substitution import free_vars, type_occurs, TypeSubstitution

a, b, c = Type(), Type(), Type()


class TestSubstitution(TestCase):
    def test_free_vars_basic(self):
        self.assertSetEqual({a}, set(free_vars(a)))

    def test_free_vars_function(self):
        self.assertSetEqual({a, b}, set(free_vars(FuncType((a,), b))))

    def test_free_vars_nested(self):
        self.assertSetEqual(
            {a, b, c},
            set(free_vars(FuncType((a,), FuncType((b,), c))))
        )

    def test_type_occurs_basic(self):
        self.assertTrue(type_occurs(a, a))

    def test_type_occurs_not_found(self):
        self.assertFalse(type_occurs(a, b))

    def test_type_occurs_nested(self):
        with self.subTest("First argument"):
            self.assertTrue(type_occurs(b, FuncType((b,), a)))
            self.assertFalse(type_occurs(b, FuncType((a,), a)))

        with self.subTest("Second argument"):
            self.assertTrue(type_occurs(b, FuncType((a, b), a)))
            self.assertFalse(type_occurs(b, FuncType((a, a), a)))

        with self.subTest("Return value"):
            self.assertTrue(type_occurs(b, FuncType((a,), b)))
            self.assertFalse(type_occurs(b, FuncType((a,), a)))

        with self.subTest("Deeply nested"):
            self.assertTrue(type_occurs(b, FuncType((FuncType((a, a), b),), FuncType((a, a), a))))
            self.assertFalse(type_occurs(b, FuncType((FuncType((a, a), a),), FuncType((a, a), a))))

    def test_type_substitution_basic(self):
        self.assertEqual(b, TypeSubstitution({a: b}).apply(a))

    def test_type_substitution_not_found(self):
        self.assertEqual(c, TypeSubstitution({a: b}).apply(c))

    def test_type_substitution_nested(self):
        with self.subTest("First argument"):
            self.assertEqual(
                FuncType((b,), c),
                TypeSubstitution({a: b}).apply(FuncType((a,), c))
            )

        with self.subTest("Second argument"):
            self.assertEqual(
                FuncType((c, b), c),
                TypeSubstitution({a: b}).apply(FuncType((c, a), c))
            )

        with self.subTest("Return value"):
            self.assertEqual(
                FuncType((c,), b),
                TypeSubstitution({a: b}).apply(FuncType((c,), a))
            )

        with self.subTest("Deeply nested"):
            self.assertEqual(
                FuncType((FuncType((c, b), b),), FuncType((b, c), c)),
                TypeSubstitution({a: b}).apply(
                    FuncType((FuncType((c, a), a),), FuncType((a, c), c))
                )
            )

    def test_type_substitution_concatenation(self):
        self.assertEqual(
            TypeSubstitution({a: c, b: c}),
            TypeSubstitution({a: b}) + TypeSubstitution({b: c})
        )

    def test_type_substitution_concatenation_order_of_operations(self):
        self.assertEqual(
            TypeSubstitution({a: b}),
            TypeSubstitution({a: b}) + TypeSubstitution({a: c})
        )

    def test_type_substitution_concatenation_remove_redundant_replacements(self):
        self.assertEqual(
            TypeSubstitution({b: a}),
            TypeSubstitution({a: b}) + TypeSubstitution({b: a})
        )

    def test_type_substitution_closure(self):
        self.assertEqual(
            TypeSubstitution({a: c, b: c}),
            TypeSubstitution({a: b, b: c}).closure()
        )
