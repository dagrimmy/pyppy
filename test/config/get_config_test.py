from argparse import ArgumentParser

from pyppy.config.get_config import initialize_config, config, destroy_config
from pyppy.utils.exc import ConfigAlreadyInitializedException
from test.utils.testcase import TestCase


class ContainerTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_config(self):
        # parse and initialize
        parser = ArgumentParser()
        parser.add_argument("--tmp1", type=str)
        parser.add_argument("--tmp2", type=int)

        cli_args = ["--tmp1", "val1", "--tmp2", "2"]

        args = parser.parse_args(cli_args)

        initialize_config(args)
        conf = config()

        self.assertEqual(conf.tmp1, "val1")
        self.assertEqual(conf.tmp2, 2)

        # new initialize should raise and
        # not overwrite previous config
        parser2 = ArgumentParser()
        parser2.add_argument("--tmp3", type=str)
        parser2.add_argument("--tmp4", type=int)

        cli_args2 = ["--tmp3", "val3", "--tmp4", "4"]
        args2 = parser2.parse_args(cli_args2)

        with self.assertRaises(ConfigAlreadyInitializedException):
            initialize_config(args2)

        self.assertEqual(conf, config())

        with self.assertRaises(AttributeError):
            config().tmp3

        with self.assertRaises(AttributeError):
            config().tmp4

        # destroy config should allow new initialize
        destroy_config()

        parser2 = ArgumentParser()
        parser2.add_argument("--tmp5", type=str)
        parser2.add_argument("--tmp6", type=int)

        cli_args3 = ["--tmp5", "val5", "--tmp6", "6"]
        args3 = parser2.parse_args(cli_args3)
        initialize_config(args3)
        conf3 = config()

        self.assertNotEqual(conf3, conf)
        self.assertEqual(conf3.tmp5, "val5")
        self.assertEqual(conf3.tmp6, 6)

        with self.assertRaises(AttributeError):
            config().tmp1

        with self.assertRaises(AttributeError):
            config().tmp2