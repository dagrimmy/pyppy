from types import SimpleNamespace

from pyppy.container.container import _Container
from pyppy.utils.exception import AlreadyInitializedException
from test.utils.testcase import TestCase


class ContainerTest(TestCase):

    def test_direct_use_of_container_class(self):
        namespace = SimpleNamespace()
        namespace.tmp1 = "val1"

        with self.assertRaises(ValueError):
            _Container.initialize(namespace)
        with self.assertRaises(ValueError):
            _Container.get()
        with self.assertRaises(ValueError):
            _Container.destroy()

    def test_double_initialization(self):
        class TmpContainer(_Container):
            name = "test_double_initialization"

        TmpContainer.initialize(SimpleNamespace())
        with self.assertRaises(AlreadyInitializedException):
            TmpContainer.initialize(SimpleNamespace())

    def test_container(self):
        class TmpContainer(_Container):
            name = "test_container"

        namespace = SimpleNamespace()
        namespace.attr_1 = "val1"

        TmpContainer.initialize(namespace)

        self.assertTrue(hasattr(TmpContainer, "test_container"))
        self.assertEqual(TmpContainer.test_container, namespace)
        self.assertEqual(TmpContainer.test_container.attr_1, "val1")

    def test_destroy(self):
        class TmpContainer(_Container):
            name = "test_destroy"

        namespace = SimpleNamespace()
        namespace.attr_1 = "val1"

        TmpContainer.initialize(namespace)

        self.assertTrue(hasattr(TmpContainer, "test_destroy"))
        self.assertEqual(TmpContainer.test_destroy, namespace)
        self.assertEqual(TmpContainer.test_destroy.attr_1, "val1")

        TmpContainer.destroy()

        self.assertFalse(hasattr(TmpContainer, "test_destroy"))

        with self.assertNotRaises(AlreadyInitializedException):
            TmpContainer.initialize(SimpleNamespace())


