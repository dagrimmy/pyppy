import doctest
import importlib
import pkgutil
import unittest
from types import ModuleType
from typing import List
import pyppy.container

import pyppy


def list_submodules(list_name: List, package: ModuleType):
    """
    Recursively finds submodules of the given package.

    Parameters
    ----------
    list_name: list
        List that found packages are appended to.
    package:
        An imported package for which to find sub modules.

    Returns
    -------
    None
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        list_name.append(module_name)
        module_name = importlib.import_module(module_name)
        if is_pkg:
            list_submodules(list_name, module_name)


class DocTest(unittest.TestCase):

    def test_doc(self):
        sub_modules = []
        list_submodules(sub_modules, pyppy)

        for submodule in sub_modules:
            submodule_import = importlib.import_module(submodule)

            test_results = doctest.testmod(submodule_import)

            self.assertEqual(test_results.failed, 0)

