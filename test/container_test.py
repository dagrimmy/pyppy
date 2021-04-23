from types import SimpleNamespace

from test.utils.testcase import TestCase
from pyppy.container import initialize, _Container, get, destroy, destroy_all


class TestContainer(TestCase):

    def setUp(self) -> None:
        pass
        # destroy_all()

    def test_initialize(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj, "config")
        self.assertIs(_Container.config, container_obj)

    def test_initialize_default(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj)
        self.assertIs(_Container.default, container_obj)

    def test_get(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj, "config")
        self.assertIs(get("config"), container_obj)

    def test_get_default(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj)
        self.assertIs(get("default"), container_obj)

    def test_destroy(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj, "config")

        self.assertIs(get("config"), container_obj)
        destroy("config")

        with self.assertRaises(AttributeError) as e:
            get("config")

        self.assertIn("'_Container' has no attribute 'config'", str(e.exception))

    def test_destroy_default(self):
        container_obj = SimpleNamespace()
        container_obj.attr_1 = "val_1"
        initialize(container_obj)

        self.assertIs(get(), container_obj)
        destroy()

        with self.assertRaises(AttributeError) as e:
            get()

        self.assertIn("'_Container' has no attribute 'default'", str(e.exception))

    def test_double_initialization_overwrite(self):
        container_obj_1 = SimpleNamespace()
        initialize(container_obj_1, "config")
        self.assertIs(get("config"), container_obj_1)

        container_obj_2 = SimpleNamespace()
        initialize(container_obj_2, "config")
        self.assertIsNot(get("config"), container_obj_1)
        self.assertIs(get("config"), container_obj_2)

    def test_destroy_all(self):
        container_obj_1 = SimpleNamespace()
        container_obj_2 = SimpleNamespace()
        container_obj_3 = SimpleNamespace()
        initialize(container_obj_1, "config_1")
        initialize(container_obj_2, "config_2")
        initialize(container_obj_3, "config_3")

        self.assertIs(get("config_1"), container_obj_1)
        self.assertIs(get("config_2"), container_obj_2)
        self.assertIs(get("config_3"), container_obj_3)

        destroy_all()

        with self.assertRaises(AttributeError) as e1:
            get("config_1")
        self.assertIn("'_Container' has no attribute 'config_1'", str(e1.exception))

        with self.assertRaises(AttributeError) as e2:
            get("config_2")
        self.assertIn("'_Container' has no attribute 'config_2'", str(e2.exception))

        with self.assertRaises(AttributeError) as e3:
            get("config_3")
        self.assertIn("'_Container' has no attribute 'config_3'", str(e3.exception))

    #
    # def test_multiple_container(self):
    #     pass
    #
    # def test_memory_behavior(self):
    #     pass
    #


