from argparse import ArgumentParser, Namespace

from pyppy.exc import StateAlreadyInitializedException
from pyppy.state import destroy_state, initialize_state, state
from test.testcase import TestCase


class StateTest(TestCase):

    def setUp(self) -> None:
        destroy_state()

    def test_state(self):
        namespace = Namespace()
        namespace.tmp1 = "val1"
        namespace.tmp2 = 2

        initialize_state(namespace)
        state_ = state()

        self.assertEqual(state_.tmp1, "val1")
        self.assertEqual(state_.tmp2, 2)

    def test_state_already_initialized(self):
        namespace = Namespace()
        namespace.tmp = "tmp"
        initialize_state(namespace)

        with self.assertRaises(StateAlreadyInitializedException):
            initialize_state(Namespace())

        self.assertEqual(namespace, state())

    def test_destroy_state(self):
        initialize_state(Namespace())
        state_ = state()

        with self.assertRaises(AttributeError):
            state_.tmp

        destroy_state()

        parser2 = ArgumentParser()
        parser2.add_argument("--tmp5", type=str)
        parser2.add_argument("--tmp6", type=int)

        cli_args3 = ["--tmp5", "val5", "--tmp6", "6"]
        args3 = parser2.parse_args(cli_args3)
        initialize_state(args3)
        state3 = state_()

        self.assertNotEqual(state3, state_)
        self.assertEqual(state3.tmp5, "val5")
        self.assertEqual(state3.tmp6, 6)

        with self.assertRaises(AttributeError):
            state_().tmp1

        with self.assertRaises(AttributeError):
            state_().tmp2