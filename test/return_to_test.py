from pyppy.return_to import return_to
from test.utils.fake_container import fake_container
from test.utils.testcase import TestCase
from pyppy.container import destroy_all, get


class TestContainer(TestCase):

    def setUp(self) -> None:
        destroy_all()

    def test(self):
        container_name = "config"
        with fake_container(container_name):

            @return_to.config(["val1", "val2", "val3"])
            def tmp():
                return "a", "b", "c"

            return_val = tmp()

            self.assertEqual(return_val, ("a", "b", "c"))

            self.assertTrue(hasattr(get["config"], "val1"))
            self.assertTrue(hasattr(get["config"], "val2"))
            self.assertTrue(hasattr(get["config"], "val3"))

            self.assertEqual(get["config"].val1, "a")
            self.assertEqual(get["config"].val2, "b")
            self.assertEqual(get["config"].val3, "c")
