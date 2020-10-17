import io
import re
import sys
from argparse import ArgumentParser

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.conditions.conditions import condition, s_, and_
from pyppy.config.get_config import destroy_config, initialize_config
from pyppy.pipeline.pipeline import step, Pipeline
from pyppy.utils.exc import MissingPipelineException, MissingConfigParamException
from test.utils.testcase import TestCase


class PipelineTest(TestCase):

    def setUp(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def tearDown(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def test_register_steps(self):

        @step("tmp")
        def tmp1():
            pass

        @step("tmp")
        def tmp2():
            pass

        @step("hurz")
        def hurz1():
            pass

        @step("hurz")
        def hurz2():
            pass

        steps = Pipeline.pipelines

        self.assertTrue("tmp" in steps)
        self.assertTrue(len(steps["tmp"]) == 2)
        self.assertTrue("tmp1" in str(steps["tmp"][0]))
        self.assertTrue("tmp2" in str(steps["tmp"][1]))

        self.assertTrue("hurz" in steps)
        self.assertTrue(len(steps["hurz"]) == 2)
        self.assertTrue("hurz1" in str(steps["hurz"][0]))
        self.assertTrue("hurz2" in str(steps["hurz"][1]))

    def test_run_pipeline(self):
        @step("tmp")
        def tmp1():
            print("func1")
            return "func1"

        @step("tmp")
        def tmp2():
            print("func2")
            return "func2"

        steps = Pipeline.pipelines

        self.assertTrue("tmp" in steps)
        self.assertTrue(len(steps["tmp"]) == 2)
        self.assertTrue("tmp1" in str(steps["tmp"][0]))
        self.assertTrue("tmp2" in str(steps["tmp"][1]))

        # temporarily redirect stdout
        old_stdout = sys.stdout
        sys.stdout = tmp_stdout = io.StringIO()
        Pipeline.run("tmp")
        sys.stdout = old_stdout
        self.assertEqual(
            re.sub(r"\s+", "", tmp_stdout.getvalue()),
            "func1func2",
        )

        with self.assertRaises(MissingPipelineException):
            Pipeline.run("ahsjdhfjaklsdf")
            Pipeline.run_r("ahsjdhfjaklsdf")

        results = [r for r in Pipeline.run_r("tmp")]
        self.assertTrue(len(results) == 2)
        self.assertTrue(results[0] == "func1")
        self.assertTrue(results[1] == "func2")

    def test_inject_from_config(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        cli_args = ["--b", "b__"]
        initialize_config(parser.parse_args(cli_args))

        result = [r for r in Pipeline.run_r("tmp")][0]
        self.assertEqual(result, "func1:a_b__")

    def test_inject_failure(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments
        def tmp1(x, b="c"):
            return f"func1:{x}{b}"

        with self.assertRaises(MissingConfigParamException):
            initialize_config(parser.parse_args(["--b", "b__"]))

            result = [r for r in Pipeline.run_r("tmp")][0]
            self.assertEqual(result, "func1:a_b__")

    def test_conditional_execution_1(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        @step("tmp")
        @condition(s_(a="_"))
        @fill_arguments
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run_r("tmp")]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], "func1:a_b__")
        self.assertEqual(result[1], None)

    def test_conditional_execution_2(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        exp = and_(
            s_(a="a_"),
            s_(b="b__")
        )

        @step("tmp")
        @condition(exp)
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run_r("tmp")]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], "func1:a_b__")
        self.assertEqual(result[1], "func2")


