from pyppy.arg_filling import Fill, fill
from test.utils.fake_container import fake_container
from test.utils.testcase import TestCase


class ArgFillingTest(TestCase):

    def test_arg_filling_roundtrip(self):
        container_name = "config"
        with fake_container(
            container_name,
            debug=True
        ):

            @Fill().config()
            def func_1(debug):
                return debug

            self.assertEqual(True, func_1())

            @fill.config()
            def func_2(debug):
                return debug

            self.assertEqual(True, func_2())

