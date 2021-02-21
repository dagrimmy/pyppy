from types import SimpleNamespace

from test.utils.testcase import TestCase
from pyppy.container import initialize, get, destroy, _Container, destroy_all


class TestContainer(TestCase):

    def setUp(self) -> None:
        destroy_all()

    def test_initialize_attr(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize.config(container_obj)
        self.assertIs(_Container.config, container_obj)

    # def test_initialize_call(self):
    #     container_obj = SimpleNamespace()
    #     container_obj.attr_1 = "val_1"
    #     initialize("config", container_obj)
    #     self.assertIs(_Container.config, container_obj)
    #
    # def test_get(self):
    #     container_obj = SimpleNamespace()
    #     container_obj.attr_1 = "val_1"
    #     initialize("config", container_obj)
    #
    #     self.assertIs(get().config, container_obj)
    #     self.assertIs(get("config")["config"], container_obj)
    #
    # def test_destroy_attr(self):
    #     container_obj = SimpleNamespace()
    #     container_obj.attr_1 = "val_1"
    #     initialize.config(container_obj)
    #
    #     self.assertIs(get.config, container_obj)
    #     destroy.config()
    #
    #     with self.assertRaises(AttributeError):
    #         get.config
    #
    # def test_destroy_call(self):
    #     container_obj = SimpleNamespace()
    #     container_obj.attr_1 = "val_1"
    #     initialize.config(container_obj)
    #
    #     self.assertIs(get.config, container_obj)
    #     destroy("config")
    #
    #     with self.assertRaises(AttributeError):
    #         get.config
    #
    # def test_empty_initialization_attr(self):
    #     initialize.config_1()
    #     self.assertIsInstance(get.config_1, SimpleNamespace)
    #     self.assertIsInstance(get["config_1"], SimpleNamespace)
    #
    # def test_empty_initialization_call(self):
    #     initialize("config_1")
    #     self.assertIsInstance(get.config_1, SimpleNamespace)
    #     self.assertIsInstance(get["config_1"], SimpleNamespace)
    #
    # def test_double_initialization_overwrite(self):
    #     container_obj_1 = SimpleNamespace()
    #     initialize.config(container_obj_1)
    #     self.assertIs(get.config, container_obj_1)
    #
    #     container_obj_2 = SimpleNamespace()
    #     initialize.config(container_obj_2)
    #
    #     self.assertIsNot(get.config, container_obj_1)
    #     self.assertIs(get.config, container_obj_2)
    #
    # def test_destroy_all(self):
    #     container_obj_1 = SimpleNamespace()
    #     container_obj_2 = SimpleNamespace()
    #     container_obj_3 = SimpleNamespace()
    #     initialize.config_1(container_obj_1)
    #     initialize.config_2(container_obj_2)
    #     initialize.config_3(container_obj_3)
    #
    #     self.assertIs(get.config_1, container_obj_1)
    #     self.assertIs(get.config_2, container_obj_2)
    #     self.assertIs(get.config_3, container_obj_3)
    #
    #     destroy_all()
    #
    #     with self.assertRaises(AttributeError):
    #         get.config_2
    #
    #     with self.assertRaises(AttributeError):
    #         get.config_3
    #
    # def test_destroy_all_conflict(self):
    #     container_obj = SimpleNamespace()
    #     initialize.all(container_obj)
    #
    #     self.assertIs(get.all, container_obj)
    #
    #     destroy_all()
    #
    #     with self.assertRaises(AttributeError):
    #         get.all
    #
    # def test_multiple_container(self):
    #     pass
    #
    # def test_memory_behavior(self):
    #     pass
    #


