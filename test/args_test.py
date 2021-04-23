from pyppy.args import _Fill, fill
from pyppy.container import destroy_all
from test.utils.fake_container import fake_container
from test.utils.testcase import TestCase


class ArgFillingTest(TestCase):

    def setUp(self) -> None:
        destroy_all()

    def test_arg_filling_all(self):
        container_name = "config"
        with fake_container(
            container_name,
            debug=True
        ):

            @fill.config()
            def func_1(debug):
                return debug

            self.assertEqual(True, func_1())

            @fill.config()
            def func_2(debug):
                return debug

            self.assertEqual(True, func_2())

    def test_explicit_arg_filling(self):
        container_name = "config"
        with fake_container(
            container_name,
            debug=True,
            log_level="WARN"
        ):

            @fill.config("debug")
            def func(debug, log_level):
                return debug, log_level

            with self.assertRaises(TypeError):
                func()

            self.assertEqual(func(log_level="INFO"), (True, "INFO"))

    def test_mulitprocessing_behavior(self):
        pass

    def test_threading_behavior(self):
        pass
