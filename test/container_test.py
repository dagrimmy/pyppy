from types import SimpleNamespace

from test.utils.testcase import TestCase
from pyppy.container import (initialize, _Container, get, destroy)


class TestContainer(TestCase):

    def test_container_roundtrip(self):
        container_name = "config"
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_name, container_obj)

        res = getattr(_Container, container_name)
        self.assertEqual(res, container_obj)
        self.assertTrue(hasattr(res, "attr_1"))
        self.assertTrue(res.attr_1, "val_1")

        res = get(container_name)
        self.assertEqual(res, container_obj)
        self.assertTrue(hasattr(res, "attr_1"))
        self.assertTrue(res.attr_1, "val_1")

        destroy("config")

        self.assertFalse(hasattr(_Container, container_name))
        with self.assertRaises(AttributeError):
            get("config")

    def test_multiple_container(self):
        pass

    def test_overwrite_container(self):
        pass

    def test_memory_behavior(self):
        pass



