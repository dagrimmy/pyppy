from argparse import ArgumentParser

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.config.get_config import initialize_config
from test.utils.testcase import TestCase


class FillArgumentsTest(TestCase):

    def test_fill_arguments(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="bbb")
        parser.add_argument("--c", default="c_")
        parser.add_argument("--d", default="ddd")
        initialize_config(parser.parse_args(["--a", "aaa", "--c", "ccc"]))

        @fill_arguments
        def tmp1(a, b):
            return f"func:{a}:{b}"

        @fill_arguments
        def tmp2(c, d):
            return f"func:{c}:{d}"

        self.assertEqual(tmp1(), "func:aaa:bbb")
        self.assertEqual(tmp2(), "func:ccc:ddd")
