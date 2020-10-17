from argparse import ArgumentParser
from collections import OrderedDict

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.conditions.conditions import condition, s_
from pyppy.config.get_config import initialize_config, destroy_config
from pyppy.pipeline.pipeline import step, Pipeline
from test.utils.testcase import TestCase


class DecoratorStackingTest(TestCase):

    def setUp(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def tearDown(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def test_decorator_stacking(self):
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        parser_sub1 = subparsers.add_parser('sub1')
        parser_sub1.add_argument('--sub1-tmp', type=int)

        parser_sub2 = subparsers.add_parser('sub2')
        parser_sub2.add_argument('--sub2-tmp', type=int)

        cli_args = ["sub1", "--sub1-tmp", "1"]
        initialize_config(parser.parse_args(cli_args))

        @step("tmp")
        @condition(s_(lambda c: c.command == "sub1"))
        @fill_arguments
        def tmp1(sub1_tmp):
            return f"func1:{sub1_tmp}"

        @step("tmp")
        @condition(s_(lambda c: c.command == "sub2"))
        @fill_arguments
        def tmp2(sub2_tmp):
            return f"func1:{sub2_tmp}"

        self.assertEqual(tmp1(), "func1:1")
        self.assertIsNone(tmp2())

        result = [r for r in Pipeline.run_r("tmp")]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "func1:1")
        self.assertIsNone(result[1][1])
