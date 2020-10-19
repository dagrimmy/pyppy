from argparse import ArgumentParser

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.config.get_config import initialize_config, destroy_config
from pyppy.config.get_container import container, destroy_container
from pyppy.utils.exc import FunctionSignatureNotSupportedException
from test.utils.testcase import TestCase


class FillArgumentsTest(TestCase):

    def setUp(self) -> None:
        destroy_container()
        destroy_config()

    def test_fill_arguments(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="bbb")
        parser.add_argument("--c", default="c_")
        parser.add_argument("--d", default="ddd")
        args = parser.parse_args(["--a", "aaa",
                                  "--c", "ccc"])
        initialize_config(args)

        @fill_arguments()
        def tmp1(a, b):
            return f"func:{a}:{b}"

        @fill_arguments()
        def tmp2(c, d):
            return f"func:{c}:{d}"

        self.assertEqual(tmp1(), "func:aaa:bbb")
        self.assertEqual(tmp2(), "func:ccc:ddd")

    def test_fill_two_args(self):
        initialize_config()
        cont = container()
        cont.arg1 = "val1"
        cont.arg2 = "val2"
        cont.arg3 = "val3"
        cont.arg4 = "val4"

        @fill_arguments()
        def tmp1(arg1, arg2):
            return f"func:{arg1}:{arg2}"

        self.assertEqual(tmp1(), "func:val1:val2")

    def test_fill_positional_arg(self):
        initialize_config()
        cont = container()
        cont.arg1 = "val1"
        cont.arg2 = "val2"
        cont.arg3 = "val3"
        cont.arg4 = "val4"

        @fill_arguments("arg3")
        def tmp2(arg3, arg4="blabla"):
            return f"func:{arg3}:{arg4}"
        self.assertEqual(tmp2(), "func:val3:blabla")
        self.assertEqual("func:val3:cool", tmp2(arg4="cool"))

    def test_fill_keyword_arg(self):
        initialize_config()
        cont = container()
        cont.arg1 = "val1"
        cont.arg2 = "val2"
        cont.arg3 = "val3"
        cont.arg4 = "val4"

        @fill_arguments("arg4")
        def tmp3(arg3, arg4="blabla"):
            return f"func:{arg3}:{arg4}"

        self.assertEqual("func:cool:val4", tmp3(arg3="cool"))

    def test_fill_keyword_arg_2(self):
        initialize_config()
        cont = container()
        cont.arg1 = "val1"
        cont.arg2 = "val2"
        cont.arg3 = "val3"
        cont.arg4 = "val4"

        @fill_arguments("arg4")
        def tmp4(arg3="tmp", arg4="blabla"):
            return f"func:{arg3}:{arg4}"

        self.assertEqual("func:cool:val4", tmp4(arg3="cool"))

    def test_raise_positional_only_args(self):
        with self.assertRaises(FunctionSignatureNotSupportedException):
            @fill_arguments("arg3", "arg4")
            def tmp4(x, y, /, arg3, arg4="blabla"):
                return f"func:{x}:{y}:{arg3}:{arg4}"

    def test_raise_keyword_only(self):
        with self.assertRaises(FunctionSignatureNotSupportedException):
            @fill_arguments()
            def tmp4(arg1, *args, arg4="blabla"):
                return f"func:{arg1}:{args}:{arg4}"

    def test_raise_var_keyword(self):
        with self.assertRaises(FunctionSignatureNotSupportedException):
            @fill_arguments()
            def tmp4(arg1, **kwargs):
                return f"func:{arg1}:{kwargs}"