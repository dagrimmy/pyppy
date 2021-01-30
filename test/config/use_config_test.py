"""
Cases:
    * Is the original class correctly decorated? Will it lose its original attribues?
    * Don't allow overriding of config_ parameters in use config_ decorated classes (config_ params should only
    be changed with config_() -> only get descriptiors (non override)
"""

from pyppy import initialize_config, config, destroy_config
from pyppy.config_.use_config import use_config
from test.utils.testcase import TestCase


class UseConfigTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_use_config(self):

        @use_config("param_1")
        class TestClass:
            pass

            def return_param(self):
                return self.param_1

        initialize_config()
        config().param_1 = "val_1"
        config().param_2 = "val_2"
        config().param_3 = "val_3"

        self.assertEqual(TestClass().param_1, "val_1")

        with self.assertRaises(AttributeError):
            TestClass().param_2

        with self.assertRaises(AttributeError):
            TestClass().param_3

        self.assertEqual(TestClass().return_param(), "val_1")