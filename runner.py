#!/usr/bin/env python3

from Tuffix.Quieter import quiet
from UnitTests.SequentialTest import SequentialTestLoader

import dataclasses
import enum
import importlib.util
import os
import pathlib
import re
import termcolor
import unittest


class Indexer(enum.Enum):
    TOTAL, FAILURE = 0, 1


class TuffixTestRunner():
    def __init__(self, parent_dir: pathlib.Path, pedantic: bool,
                 excluded_files: list = [
                     "SequentialTest.py", "__init__.py", "BaseTester.py", "README.md"],
                 excluded_dirs: list = ["__pycache__", "TEST"]):
        if not(isinstance(parent_dir, pathlib.Path) and
               parent_dir.is_dir() and
               isinstance(pedantic, bool) and
               isinstance(excluded_files, list) and
               all([isinstance(_, str) for _ in excluded_files]) and
               isinstance(excluded_dirs, list) and
               all([isinstance(_, str) for _ in excluded_dirs])):
            raise ValueError

        self.runner = unittest.TextTestRunner()
        self.pedantic = pedantic
        self.indexer = Indexer()
        self.score = [0, 0]
        self.excluded_files = excluded_files
        self.excluded_dirs = excluded_dirs
        self.file_system = self.construct_filesystem()

    def construct_filesystem(self, pedantic: bool = self.pedantic):
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

        container = []

        for dirpath, dirs, filepath in os.walk(self.parent_dir, topdown=True):
            dirs.sort()
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            filepath[:] = [f for f in filepath if f not in self.excluded_files]
            test_name = os.path.basename(dirpath)
            if not(test_name == str(self.parent_dir)):
                filepath = [(pathlib.Path(self.parent_dir / path),
                             self.pedantic) for path in filepath]
                container.append(
                    {test_name: filepath}
                )
        self.file_system = container

    def test_certain_class(self, name: str):
        """
        Test certain module from Tuffix:
        Example: Tuffix.Editors
        """

        if not(isinstance(name, str)):
            raise ValueError
        try:
            test_suite = self.file_system[name]
        except KeyError:
            print(f'[ERROR] Could not find test {test_suite}')
        for __test in test_suite:
            self.conduct_test(__test)

    def conduct_test(self, path: pathlib.Path):
        """
        Run the test given a path to the module and if it will be pendantic
        """

        if not(isinstance(path, pathlib.Path)):
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
            return [0, 0]

        # these tests names must conform to a certain format
        # for example: ExampleTest
        # not working example: SomethingOrAnother

        tests = [_test for _test in dir(module) if (test_re.match(_test))]
        counter = [0, 0]

        for _test in tests:
            print(f'[INFO] Conducting {_test}')
            # get the current instance of the class we are interested in
            test_instance = getattr(module, _test, None)
            # load the current test into a testloader for unittest
            test_suite = SequentialTestLoader().loadTestsFromTestCase(test_instance)

            total_test_count = test_suite.countTestCases()

            counter[Indexer.TOTAL.value] += total_test_count

            # send all output from functions to /dev/null if specified

            if(self.pedantic):
                result = runner.run(test_suite)
            else:
                with quiet():
                    result = self.runner.run(test_suite)
            counter[Indexer.FAILURE.value] += (len(result.failures))

        return counter

    def run_tests(self):
        """
        Driver code for the two functions above
        """

        total_counter = [0, 0]
        tests = self.construct_filesystem(pedantic=self.pedantic)
        for test in tests:
            for name, arguments in test.items():
                for subtest, pedantic in arguments:
                    path = (self.parent_dir / name / subtest)
                    result = conduct_test(path, pedantic)
                    total_counter[self.Indexer.TOTAL.value] += result[self.Indexer.TOTAL.value]
                    total_counter[self.Indexer.FAILURE.value] += result[self.Indexer.FAILURE.value]

        total, failures = total_counter
        if(failures == 0):
            print(termcolor.colored(
                f'All {total} test(s) have all passed', 'green'
            ))
        else:
            print(termcolor.colored(
                f'{total - failures}/{total} test(s) have passed', 'red'
            ))


# cache this so it doesn't run all of them at once
# run_tests()
# conduct_test(
    # pathlib.Path("UnitTests/TEST/Editors/test_emacs_editor.py"),
    # True
# )

R = TuffixTestRunner(
    parent_dir=pathlib.Path("UnitTests/"),
    pedantic=True
)
