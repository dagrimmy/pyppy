from pyppy.use import use
from test.utils.fake_container import fake_container
from test.utils.testcase import TestCase
from pyppy.container import destroy_all


class TestContainer(TestCase):

    def setUp(self) -> None:
        destroy_all()

    def test_use(self):
        container_name = "config"
        with fake_container(
            container_name,
            debug=True,
            log_level="WARN"
        ):

            @use.config("debug", "log_level")
            class Class1:
                pass

            self.assertTrue(hasattr(Class1, "debug"))
            self.assertTrue(hasattr(Class1, "log_level"))
            self.assertEqual(Class1.debug, True)
            self.assertEqual(Class1.log_level, "WARN")
