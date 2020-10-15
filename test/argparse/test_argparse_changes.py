import argparse

from test.utils.testcase import TestCase


class ArgparseTest(TestCase):

    """
        This test is mainly for testing the behavior of argparse.
        If tests fail we know argparse has changed and we might
        have to do some modifications.

        Also, these tests helped me during the development
        which features of argparse have to be supported by
        pyppy.
    """

    def test_standard_arg(self):
        args = ["--int", "1", "2"]
        parser = argparse.ArgumentParser(description="Test")
        parser.add_argument(
            "--ints",
            type=int,
            nargs="+",
        )

        parsed_args = parser.parse_args(args)

        self.assertEqual(parsed_args.ints, [1, 2])

    def test_destination_arg(self):
        parser = argparse.ArgumentParser(description="Test")
        parser.add_argument(
            "--yes",
            action="store_const",
            dest="yesssss",
            const=True,
            default=False,
            help="Do it!",
        )

        parsed_args = parser.parse_args(["--yes"])
        self.assertEqual(parsed_args.yesssss, True)

    def test_destination_arg_default(self):
        parser = argparse.ArgumentParser(description="Test")
        parser.add_argument(
            "--yes",
            action="store_const",
            dest="yesssss",
            const=True,
            default=False,
            help="Do it!",
        )

        parsed_args = parser.parse_args([])
        self.assertEqual(parsed_args.yesssss, False)

    def test_parents(self):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('--parent', type=int)

        child1_parser = argparse.ArgumentParser(parents=[parent_parser])
        child1_parser.add_argument('--tmp1')
        args1 = child1_parser.parse_args(['--parent', "1", "--tmp1", "val1"])

        self.assertEqual(args1.parent, 1)
        self.assertEqual(args1.tmp1, "val1")

        child2_parser = argparse.ArgumentParser(parents=[parent_parser])
        child2_parser.add_argument('--tmp2')
        args2 = child2_parser.parse_args(['--parent', "2", "--tmp2", "val2"])

        self.assertEqual(args2.parent, 2)
        self.assertEqual(args2.tmp2, "val2")

    def test_default_suppress(self):
        parser = argparse.ArgumentParser(prefix_chars="-+")
        parser.add_argument('--tmp')
        parser.add_argument('++tmp')

        self.assertTrue(parser.parse_args(["--tmp", "val"]))
        self.assertTrue(parser.parse_args(["++tmp", "val"]))

        parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

        parser.add_argument('--tmp')
        parser.parse_args(['--tmp', "val"])

        args = parser.parse_args()
        self.assertTrue(not hasattr(args, "tmp"))

    def test_abbrev(self):
        parser1 = argparse.ArgumentParser(allow_abbrev=True)
        parser1.add_argument('--tmptmptmp')
        args1 = parser1.parse_args(['--tmp', "val"])
        self.assertEqual(args1.tmptmptmp, "val")

        parser2 = argparse.ArgumentParser(allow_abbrev=False)
        parser2.add_argument('--tmptmptmp')

        with self.assertRaises(SystemExit):
            parser2.parse_args(['--tmp'])

    def test_name_or_flags(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-tmp1")
        parser.add_argument("--tmp2")
        parser.add_argument("tmp3")
        args = parser.parse_args(["-tmp1", "val1",
                                  "--tmp2", "val2",
                                  "val3"])

        self.assertEqual(args.tmp1, "val1")
        self.assertEqual(args.tmp2, "val2")
        self.assertEqual(args.tmp3, "val3")

    def test_action(self):
        # store
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp1')
        args = parser.parse_args('--tmp1 val1'.split())
        self.assertEqual(args.tmp1, "val1")

        # store const
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp1', action='store_const', const=42)
        args = parser.parse_args(['--tmp1'])
        self.assertEqual(args.tmp1, 42)

        # store_true, store_false
        parser = argparse.ArgumentParser()
        parser.add_argument('--true', action='store_true')
        parser.add_argument('--false', action='store_false')
        parser.add_argument('--def_true', action='store_false')
        args = parser.parse_args('--true --false'.split())
        self.assertEqual(args.true, True)
        self.assertEqual(args.false, False)
        self.assertEqual(args.def_true, True)

        # append
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp', action='append')
        args = parser.parse_args('--tmp 1 --tmp 2'.split())
        self.assertEqual(args.tmp, ["1", "2"])

        # append_const
        parser = argparse.ArgumentParser()
        parser.add_argument('--str', dest='types', action='append_const', const=str)
        parser.add_argument('--int', dest='types', action='append_const', const=int)
        args = parser.parse_args('--str --int'.split())
        self.assertEqual(args.types, [str, int])

        # count
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', '-v', action='count', default=0)
        args = parser.parse_args(['-vvv'])
        self.assertEqual(args.verbose, 3)

        # extend
        parser = argparse.ArgumentParser()
        parser.add_argument("--tmp", action="extend", nargs="+", type=str)
        args = parser.parse_args(["--tmp", "f1", "--tmp", "f2", "f3", "f4"])
        self.assertEqual(args.tmp, ["f1", "f2", "f3", "f4"])

    def test_nargs(self):
        # int
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp', nargs=2)
        args = parser.parse_args('--tmp a b'.split())
        self.assertEqual(args.tmp, ["a", "b"])

        # ?
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp', nargs='?')
        args = parser.parse_args("--tmp 1".split())
        self.assertEqual(args.tmp, "1")

        args = parser.parse_args("--tmp".split())
        self.assertIsNone(args.tmp)

        # *
        parser = argparse.ArgumentParser()
        parser.add_argument('--tmp', nargs='*')
        args = parser.parse_args("--tmp 1 2 3".split())
        self.assertEqual(args.tmp, ["1", "2", "3"])

        args = parser.parse_args("--tmp 1".split())
        self.assertEqual(args.tmp, ["1"])
