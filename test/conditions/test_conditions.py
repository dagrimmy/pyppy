from pyppy.conditions.conditions import condition, s_
from test.utils.testcase import TestCase
from test.utils.testing import get_fake_argparse_namespace
from pyppy.config.get_config import initialize_config, destroy_config, config


class ConditionsTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_single_condition_true(self):

        @condition(s_(lambda c: c.tmp1 == 1))
        def tmp():
            return "returned"

        args = get_fake_argparse_namespace([
            ("tmp1", 1)
        ])

        initialize_config(args)
        self.assertTrue(tmp() == "returned")

    def test_single_condition_false(self):

        @condition(s_(lambda c: c.tmp1 == 2))
        def tmp():
            return "returned"

        args = get_fake_argparse_namespace([
            ("tmp1", 1)
        ])

        initialize_config(args)
        self.assertIsNone(tmp())

