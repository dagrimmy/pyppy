from pyppy.config.get_container import container, destroy_container
from test.utils.testcase import TestCase


class ContainerTest(TestCase):

    def setUp(self) -> None:
        destroy_container(destroy_all=True)

    def test_global_container(self):
        cont = container()
        cont.tmp1 = "tmp1"
        cont.tmp2 = "tmp2"
        self.assertEqual(container().tmp1, "tmp1")
        self.assertEqual(container().tmp2, "tmp2")

        destroy_container()

        with self.assertRaises(AttributeError):
            container().tmp1

        with self.assertRaises(AttributeError):
            container().tmp2

    def test_container_with_name(self):
        cont = container("test")
        cont.tmp1 = "tmp1"
        cont.tmp2 = "tmp2"
        self.assertEqual(container("test").tmp1, "tmp1")
        self.assertEqual(container("test").tmp2, "tmp2")

        destroy_container("test")

        with self.assertRaises(AttributeError):
            container("test").tmp1

        with self.assertRaises(AttributeError):
            container("test").tmp2

    def test_container_dont_interfere(self):
        cont = container("test1")
        cont.tmp1 = "tmp1"
        cont.tmp2 = "tmp2"
        self.assertEqual(container("test1").tmp1, "tmp1")
        self.assertEqual(container("test1").tmp2, "tmp2")

        cont = container("test2")
        cont.tmp1 = "tmp11"
        cont.tmp2 = "tmp22"
        self.assertEqual(container("test2").tmp1, "tmp11")
        self.assertEqual(container("test2").tmp2, "tmp22")
        self.assertEqual(container("test1").tmp1, "tmp1")
        self.assertEqual(container("test1").tmp2, "tmp2")

        destroy_container("test1")

        self.assertEqual(container("test2").tmp1, "tmp11")
        self.assertEqual(container("test2").tmp2, "tmp22")

        with self.assertRaises(AttributeError):
            container("test1").tmp1

        with self.assertRaises(AttributeError):
            container("test1").tmp2

    def test_no_raise_when_container_not_there(self):
        with self.assertNotRaises(AttributeError):
            destroy_container("asdjfklasjdöcjkslödj")