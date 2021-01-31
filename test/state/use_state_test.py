from pyppy import initialize_state, state, destroy_state
from pyppy.attr_filling.use_state import use_state
from test.utils.testcase import TestCase


class UseStateTest(TestCase):

    def setUp(self) -> None:
        destroy_state()

    def test_use_state(self):

        @use_state("param_1")
        class TestClass:
            pass

            def return_param(self):
                return self.param_1

        initialize_state()
        state().param_1 = "val_1"
        state().param_2 = "val_2"
        state().param_3 = "val_3"

        self.assertEqual(TestClass().param_1, "val_1")

        with self.assertRaises(AttributeError):
            TestClass().param_2

        with self.assertRaises(AttributeError):
            TestClass().param_3

        self.assertEqual(TestClass().return_param(), "val_1")