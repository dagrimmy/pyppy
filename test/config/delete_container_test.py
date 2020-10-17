from pyppy.config.get_container import container, _CONTAINER, destroy_container
from test.utils.testcase import TestCase


class ContainerTest(TestCase):

    """
    Separated from other tests because the some tests
    use this function in their setUp function as
    prerequisite. So the test if the container
    destroy function works as expected should not
    be called in the class where the functions is used
    in the setUp function.
    """

    def test_delete_all_container(self):
        container()
        container("tmp1")
        container("tmp2")

        self.assertTrue(hasattr(container, _CONTAINER))
        self.assertTrue(hasattr(container, "tmp1"))
        self.assertTrue(hasattr(container, "tmp2"))

        destroy_container(destroy_all=True)

        self.assertFalse(hasattr(container, _CONTAINER))
        self.assertFalse(hasattr(container, "tmp1"))
        self.assertFalse(hasattr(container, "tmp2"))

    def test_delete_one_container(self):
        container()
        container("tmp1")
        container("tmp2")

        self.assertTrue(hasattr(container, _CONTAINER))
        self.assertTrue(hasattr(container, "tmp1"))
        self.assertTrue(hasattr(container, "tmp2"))

        destroy_container(destroy_all=False)

        self.assertFalse(hasattr(container, _CONTAINER))
        self.assertTrue(hasattr(container, "tmp1"))
        self.assertTrue(hasattr(container, "tmp2"))

        destroy_container("tmp1")

        self.assertFalse(hasattr(container, _CONTAINER))
        self.assertFalse(hasattr(container, "tmp1"))
        self.assertTrue(hasattr(container, "tmp2"))
