from types import SimpleNamespace

from test.utils.testcase import TestCase
from pyppy.container import container, Container, _Container


class TestContainer(TestCase):

    def setUp(self) -> None:
        container.destroy_all()

    def test_container_roundtrip(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        container.config.initialize(container_obj)

        res = container.config()
        self.assertIs(res, container_obj)
        self.assertTrue(hasattr(res, "attr_1"))
        self.assertTrue(res.attr_1, "val_1")

        self.assertIs(container["config"], container_obj)

        del container.config

        self.assertIsNot(container.config(), container_obj)
        self.assertIsInstance(container.config(), SimpleNamespace)

        with self.assertRaises(AttributeError):
            container.config().attr_1

    def test_empty_initialization(self):
        container.config_1.initialize()
        self.assertIsInstance(container.config_1(), SimpleNamespace)
        self.assertIsInstance(container["config_1"], SimpleNamespace)

        container.config_2.initialize(None)
        self.assertIsInstance(container.config_2(), SimpleNamespace)
        self.assertIsInstance(container["config_2"], SimpleNamespace)

    def test_double_initialization_overwrite(self):
        container_obj_1 = SimpleNamespace()
        container.config.initialize(container_obj_1)
        self.assertIs(container.config(), container_obj_1)

        container_obj_2 = SimpleNamespace()
        container.config.initialize(container_obj_2)

        self.assertIsNot(container.config(), container_obj_1)
        self.assertIs(container.config(), container_obj_2)

    def test_multiple_container(self):
        pass

    def test_overwrite_container(self):
        pass

    def test_memory_behavior(self):
        pass



"""
container.config.initialize(obj123)
container.config -> obj123
container.config.destroy
container["config"] -> obj123

"""

