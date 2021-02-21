from pyppy.conditions import condition, Exp
from pyppy.container import destroy_all
from test.utils.fake_container import fake_container
from test.utils.testcase import TestCase


class ConditionsTest(TestCase):

    def setUp(self) -> None:
        destroy_all()

    def test_conditions(self):
        container_name = "config"
        with fake_container(
            container_name,
            debug=True
        ):

            @condition(Exp(debug=True))
            def func_1():
                return "executed"

            self.assertEqual(func_1(), "executed")

            @condition.config(Exp(debug=False))
            def func_2():
                return "executed"

            self.assertEqual(func_2(), None)
