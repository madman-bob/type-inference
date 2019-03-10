from unittest import TestCase

from type_inference.types import Type, NamedType, FuncType, AbstractType, BOOL, INT, type_simplicity
from type_inference.typing_environment import TypingEnvironment

a, b = Type(), Type()


class TestTypingEnvironment(TestCase):
    def test_typing_environment_builtins(self):
        typing_environment = TypingEnvironment()

        self.assertEqual(BOOL, typing_environment[True])
        self.assertEqual(INT, typing_environment[0])

    def test_typing_environment_get_variable_type(self):
        typing_environment = TypingEnvironment({'x': a})

        self.assertEqual(a, typing_environment['x'])

    def test_typing_environment_get_new_type(self):
        typing_environment = TypingEnvironment()

        new_type = typing_environment['x']

        self.assertIsInstance(new_type, NamedType)
        self.assertNotIn(new_type, [BOOL, INT])
        self.assertTrue(type_simplicity.compare(a, new_type))
        self.assertEqual(new_type, typing_environment['x'])
        self.assertNotEqual(new_type, typing_environment['y'])

    def test_typing_environment_get_function_evaluation_type(self):
        typing_environment = TypingEnvironment({'f': BOOL ** BOOL})

        self.assertEqual(BOOL, typing_environment['f', True])

    def test_typing_environment_get_inconsistent_type(self):
        typing_environment = TypingEnvironment({'x': BOOL})

        with self.assertRaises(TypeError):
            typing_environment['x', 0]

    def test_typing_environment_assign_type(self):
        typing_environment = TypingEnvironment()

        typing_environment['x'] = a

        self.assertEqual(a, typing_environment['x'])

    def test_typing_environment_infer_func_type(self):
        typing_environment = TypingEnvironment()

        typing_environment['f', 0] = BOOL

        self.assertEqual(INT ** BOOL, typing_environment['f'])

    def test_typing_environment_substitute_type_basic(self):
        typing_environment = TypingEnvironment()

        typing_environment['x'] = a
        typing_environment.apply_type_substitution(b / a)

        self.assertEqual(b, typing_environment['x'])

    def test_typing_environment_substitute_type_nested(self):
        with self.subTest("First argument"):
            typing_environment = TypingEnvironment()
            typing_environment['f'] = FuncType((a,), BOOL)

            typing_environment.apply_type_substitution(b / a)

            self.assertEqual(
                FuncType((b,), BOOL),
                typing_environment['f']
            )

        with self.subTest("Second argument"):
            typing_environment = TypingEnvironment()
            typing_environment['f'] = FuncType((INT, a), BOOL)

            typing_environment.apply_type_substitution(b / a)

            self.assertEqual(
                FuncType((INT, b), BOOL),
                typing_environment['f']
            )

        with self.subTest("Return value"):
            typing_environment = TypingEnvironment()
            typing_environment['f'] = FuncType((INT,), a)

            typing_environment.apply_type_substitution(b / a)

            self.assertEqual(
                FuncType((INT,), b),
                typing_environment['f']
            )

        with self.subTest("Deeply nested"):
            typing_environment = TypingEnvironment()
            typing_environment['f'] = FuncType((FuncType((INT, INT), a),), FuncType((INT, a), INT))

            typing_environment.apply_type_substitution(b / a)

            self.assertEqual(
                FuncType((FuncType((INT, INT), b),), FuncType((INT, b), INT)),
                typing_environment['f']
            )

    def test_typing_environment_substitute_type_nested_replacement(self):
        typing_environment = TypingEnvironment()

        typing_environment['f'] = a
        typing_environment.apply_type_substitution(INT ** BOOL / a)

        self.assertEqual(
            INT ** BOOL,
            typing_environment['f']
        )

    def test_typing_environment_remove_redundant_types(self):
        typing_environment = TypingEnvironment()

        typing_environment['x'] = a
        typing_environment['f'] = FuncType((a,), a)
        typing_environment['f', 'x'] = BOOL

        self.assertNotEqual(BOOL, a)
        self.assertEqual(BOOL, typing_environment['x'])
        self.assertEqual(
            FuncType((BOOL,), BOOL),
            typing_environment['f']
        )

    def test_typing_environment_infer_abstract_type(self):
        a = AbstractType()
        typing_environment = TypingEnvironment()

        typing_environment['f'] = FuncType((a,), a)
        typing_environment['f', 'x'] = BOOL
        typing_environment['f', 'y'] = INT

        self.assertEqual(BOOL, typing_environment['x'])
        self.assertEqual(INT, typing_environment['y'])
        self.assertEqual(FuncType((a,), a), typing_environment['f'])

    def test_typing_environment_eval_abstract_type(self):
        a_ = AbstractType()
        typing_environment = TypingEnvironment()

        typing_environment['f'] = FuncType((a_,), a_)

        self.assertEqual(BOOL, typing_environment['f', True])
        self.assertEqual(INT, typing_environment['f', 0])
        self.assertEqual(FuncType((a_,), a_), typing_environment['f'])
