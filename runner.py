#!/usr/bin/env python3

from Tuffix.Quieter import quiet
from UnitTests.SequentialTest import SequentialTestLoader

import unittest
import importlib.util
import os
import pathlib
import re
import pickle

runner = unittest.TextTestRunner()


def construct_filesystem(pedantic):
    """
    Read the contents of `UnitTests` and attempt to construct
    a working structure to load all valid tests

    We can also specify which directories/files should be ignored
    during construction.

    pedantic: allows for the test to print to stdout/stderr. This can be toggled to
        False to allow for less output.

    """

    if not(isinstance(pedantic, bool)):
        raise ValueError(f'{pedantic=} is not a `bool`')

    parent_dir = pathlib.Path("UnitTests")

    excluded_dirs = ["__pycache__", "TEST"]
    excluded_files = ["SequentialTest.py", "__init__.py", "BaseTester.py", "README.md"]
    container = []

    for dirpath, dirs, filepath in os.walk(parent_dir, topdown=True):
        dirs.sort()
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        filepath[:] = [f for f in filepath if f not in excluded_files]
        test_name = os.path.basename(dirpath)
        if not(test_name == str(parent_dir)):
            filepath = [(path, pedantic) for path in filepath]
            container.append(
                {test_name: filepath}
            )
    return container


def conduct_test(path: pathlib.Path, pedantic: bool):
    """
    Run the test given a path to the module and if it will be pendantic
    """

    if not(isinstance(path, pathlib.Path) and
           isinstance(pedantic, bool)):
        raise ValueError(f'{path=} is not a `pathlib.Path`')
    test_re = re.compile(".*Test")

    # get the specifications from the path given
    spec = importlib.util.spec_from_file_location("test", path)
    # load the specifications as a module to be imported
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if(hasattr(module, 'IGNORE_ME')):
        # to make testing go by quicker
        # please remove `IGNORE_ME = True` from all instances

        print(f'[INFO] Ignoring {path}')
        return

    # these tests names must conform to a certain format
    # for example: ExampleTest
    # not working example: SomethingOrAnother

    tests = [_test for _test in dir(module) if (test_re.match(_test))]

    for _test in tests:
        print(f'[INFO] Conducting {_test}')
        # get the current instance of the class we are interested in
        test_instance = getattr(module, _test, None)
        # load the current test into a testloader for unittest
        test_suite = SequentialTestLoader().loadTestsFromTestCase(test_instance)
        # send all output from functions to /dev/null if specified
        if(pedantic):
            runner.run(test_suite)
        else:
            with quiet():
                runner.run(test_suite)


def run_tests():
    """
    Driver code for the two functions above
    """

    tests = construct_filesystem(pedantic=True)
    base_folder = pathlib.Path("UnitTests")
    for test in tests:
        for name, arguments in test.items():
            for subtest, pedantic in arguments:
                path = (base_folder / name / subtest)
                conduct_test(path, pedantic)


# cache this so it doesn't run all of them at once
run_tests()
