import argparse
import sys
from unittest.mock import patch

from test.utils.testcase import TestCase


class ArgparseTest(TestCase):

    def test_standard_arg(self):
        args = ["<file>", "--int", "1", "2"]

        with patch.object(sys, 'argv', args):
            parser = argparse.ArgumentParser(description="Test")
            parser.add_argument(
                "--ints",
                type=int,
                nargs="+",
            )

            parsed_args = parser.parse_args()

            self.assertEqual(parsed_args.ints, [1, 2])

    def test_destination_arg(self):
        args = ["<file>", "--yes"]

        with patch.object(sys, 'argv', args):
            parser = argparse.ArgumentParser(description="Test")
            parser.add_argument(
                "--yes",
                action="store_const",
                dest="yesssss",
                const=True,
                default=False,
                help="Do it!",
            )

            parsed_args = parser.parse_args()
            self.assertEqual(parsed_args.yesssss, True)

    def test_destination_arg_default(self):
        args = ["<file>"]

        with patch.object(sys, 'argv', args):
            parser = argparse.ArgumentParser(description="Test")
            parser.add_argument(
                "--yes",
                action="store_const",
                dest="yesssss",
                const=True,
                default=False,
                help="Do it!",
            )

            parsed_args = parser.parse_args()
            self.assertEqual(parsed_args.yesssss, False)

