from argparse import Namespace

from pyppy.utils.exception import UnexpectedNumberOfReturnsException
from pyppy.state_.return_to_state import return_to_state
from pyppy import destroy_state, initialize_state, state
from test.utils.testcase import TestCase


class ReturnToStateTest(TestCase):

    def setUp(self) -> None:
        destroy_state()

    def test_single_return_to_state(self):
        namespace = Namespace()
        initialize_state(namespace)

        @return_to_state(["return_a"])
        def func():
            return "aaa"

        return_a = func()
        self.assertEqual(state().return_a, "aaa")
        self.assertEqual(return_a, "aaa")

    def test_double_return_to_state(self):
        namespace = Namespace()
        initialize_state(namespace)

        @return_to_state(["return_a", "return_b"])
        def func():
            return "aaa", "bbb"

        return_a, return_b = func()
        self.assertEqual(state().return_a, "aaa")
        self.assertEqual(state().return_b, "bbb")
        self.assertEqual(return_a, "aaa")
        self.assertEqual(return_b, "bbb")

    def test_complext_return_statements(self):
        namespace = Namespace()
        initialize_state(namespace)

        @return_to_state(arg_names=["one", "two"])
        def func(arg):
            if arg == 1:
                return 1
            elif arg == 2:
                return 1, 2
            elif arg == 3:
                return 1, 2, 3

        with self.assertRaises(UnexpectedNumberOfReturnsException):
            func(1)

        with self.assertRaises(UnexpectedNumberOfReturnsException):
            func(3)

        with self.assertNotRaises(UnexpectedNumberOfReturnsException):
            func(2)

    def test_wrong_indices(self):
        namespace = Namespace()
        initialize_state(namespace)

        @return_to_state(arg_names=["one", "two"], args_to_return_to_state=[2, 3])
        def func():
            return 1, 2

        with self.assertRaises(IndexError):
            func()

    def test_specific_values_return_to_state(self):
        namespace = Namespace()
        initialize_state(namespace)

        @return_to_state(["return_a", "_", "return_c"], [0, 2])
        def func():
            return "aaa", "bbb", "ccc"

        return_a, return_b, return_c = func()
        self.assertTrue(hasattr(state(), "return_a"))
        self.assertEqual(state().return_a, "aaa")

        self.assertFalse(hasattr(state(), "return_b"))

        self.assertTrue(hasattr(state(), "return_c"))
        self.assertEqual(state().return_c, "ccc")

        self.assertEqual(return_a, "aaa")
        self.assertEqual(return_b, "bbb")
        self.assertEqual(return_c, "ccc")