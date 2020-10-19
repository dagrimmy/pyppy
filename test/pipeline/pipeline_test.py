import io
import re
import sys
from argparse import ArgumentParser

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.conditions.conditions import condition, exp, and_
from pyppy.config.get_config import destroy_config, initialize_config
from pyppy.pipeline.pipeline import step, Pipeline
from pyppy.utils.exc import MissingPipelineException, MissingConfigParamException, PipelineAlreadyExistsException
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
        @step("tmp", "first")
        def tmp1():
            print("func1")
            return "func1"

        @step("tmp", "second")
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
        self.assertTrue(results[0] == ("first", "func1"))
        self.assertTrue(results[1] == ("second", "func2"))

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
        self.assertEqual(result, ("tmp1", "func1:a_b__"))

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

        @step("tmp", "first")
        @fill_arguments
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        @step("tmp", "second")
        @condition(exp(a="_"))
        @fill_arguments
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run_r("tmp")]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], ("first", "func1:a_b__"))
        self.assertEqual(result[1], ("second", None))

    def test_conditional_execution_2(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp", "first")
        @fill_arguments
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        exp = and_(
            exp(a="a_"),
            exp(b="b__")
        )

        @step("tmp", "second")
        @condition(exp)
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run_r("tmp")]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], ("first", "func1:a_b__"))
        self.assertEqual(result[1], ("second", "func2"))

    def test_create_pipeline_from_iterable(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        result = [r for r in Pipeline.run_r("iter-tmp")]

        self.assertTrue(len(result) == 3)
        self.assertEqual(result[0][1], "1")
        self.assertEqual(result[1][1], "2")
        self.assertEqual(result[2][1], "3")

    def test_pipeline_dict_results(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        result = dict([r for r in Pipeline.run_r("iter-tmp")])

        self.assertTrue(len(result) == 3)
        self.assertEqual(result["tmp-1"], "1")
        self.assertEqual(result["tmp-2"], "2")
        self.assertEqual(result["tmp-3"], "3")

    def test_pipeline_already_exists(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("tmp", [("tmp-1", tmp1)])

        with self.assertRaises(PipelineAlreadyExistsException):
            Pipeline.create_pipeline("tmp", [("tmp-2", tmp2)])

        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 1)

        with self.assertRaises(PipelineAlreadyExistsException):
            Pipeline.create_pipeline("tmp", [("tmp-3", tmp3)], extend=False)

        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 1)

        Pipeline.create_pipeline("tmp", [("tmp-2", tmp2), ("tmp-3", tmp3)], extend=True)
        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 3)

        result = dict(Pipeline.run_r("tmp"))
        self.assertEqual(result["tmp-1"], "1")
        self.assertEqual(result["tmp-2"], "2")
        self.assertEqual(result["tmp-3"], "3")