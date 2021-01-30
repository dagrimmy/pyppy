"""
Cases:
    * Is the original class correctly decorated? Will it lose its original attribues?
    * Don't allow overriding of config parameters in use config decorated classes (config params should only
    be changed with config() -> only get descriptiors (non override)
"""

from pyppy.config import initialize_config, config
from pyppy.use_config import use_config
from test.testcase import TestCase


class UseConfigTest(TestCase):

    def test_use_config(self):

        @use_config("param_1")
        class TestClass:
            pass

        initialize_config()
        config().param_1 = "val_1"
        config().param_2 = "val_2"
        config().param_3 = "val_3"

        self.assertEqual(TestClass().param_1, "val_1")

        with self.assertRaises(AttributeError):
            TestClass().param_2

        with self.assertRaises(AttributeError):
            TestClass().param_3