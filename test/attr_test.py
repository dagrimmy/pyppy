"""
Think about not allowing to set attrs
"""

from pyppy.config import initialize_config, config, destroy_config
from pyppy.use_config import Attr
from test.testcase import TestCase


class AttrTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_attr(self):
        initialize_config()
        config().attr = "val"

        class TestClass:

            attr = Attr("attr")

        instance_1 = TestClass()
        self.assertEqual(instance_1.attr, "val")

        config().attr = "new_val"

        self.assertEqual(TestClass().attr, "new_val")
        self.assertEqual(instance_1.attr, "new_val")

    def test_overwrite_attr(self):
        initialize_config()
        config().attr = "val"

        class TestClass:
            attr = Attr("attr")

        instance_1 = TestClass()
        instance_1.attr = "tmp"

        self.assertEqual(instance_1.attr, "tmp")
        self.assertEqual(TestClass.attr, "val")
        self.assertEqual(config().attr, "val")