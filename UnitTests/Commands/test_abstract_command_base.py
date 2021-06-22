#!/usr/bin/env python3.9

from Tuffix.Commands import AbstractCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest
import functools
import textwrap


def partial_class(container: tuple):
    build_config, name, description = container
    body = {
        "__init__": functools.partialmethod(
            AbstractCommand.__init__,
            build_config=build_config,
            name=name,
            description=description
        )
    }

    return type("test", (AbstractCommand, ), body)


class AbstractCommandTest(unittest.TestCase):
    """
    This tests the __init__ constructor with valid arguments
    """

    def test_init_valid(self):
        try:
            _ = AbstractCommand(
                DEFAULT_BUILD_CONFIG,
                'test',
                'this is a test description')
        except ValueError:
            self.assertTrue(False)

    def test_init_invalid(self):
        """
        This tests the __init__ constructor with invalid arguments
        """

        instances = [
            partial_class((DEFAULT_BUILD_CONFIG, "TEST",
                          "this is a test description")),  # captial name
            partial_class((DEFAULT_BUILD_CONFIG,
                           "test_not_working",
                           "this is a test description")),
            # non-alphanumeric characters
            partial_class((DEFAULT_BUILD_CONFIG, "",
                          "this is a test description")),  # empty name
            # BuildConfig is a float
            partial_class((0.5, "TEST", "this is a test description")),
            # description is a float
            partial_class((DEFAULT_BUILD_CONFIG, "TEST", 0.5)),
        ]

        for instance in instances:
            try:
                instance()
            except ValueError:
                self.assertTrue(True)
            else:
                self.assertTrue(False)

    def test_repr(self):
        """
        Test if the __repr__ function works
        """

        message = """
        Name: test
        Description: this is a test description
        """

        AbstractCommandTest = AbstractCommand(
            DEFAULT_BUILD_CONFIG, 'test', 'this is a test description')
        self.assertTrue(message == AbstractCommandTest.__repr__())

    def test_execute(self):
        AbstractCommandTest = AbstractCommand(
            DEFAULT_BUILD_CONFIG, 'test', 'this is a test description')
        try:
            AbstractCommandTest.execute([])
        except NotImplementedError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
