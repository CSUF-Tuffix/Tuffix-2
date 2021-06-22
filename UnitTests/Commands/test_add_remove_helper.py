#!/usr/bin/env python3.9

from Tuffix.Commands import AddRemoveHelper
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest
import functools
import textwrap


def partial_class(container: tuple):
    # NOTE : please include this in all derived classes
    # Duplicate code

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

class AddRemoveHelperTest(unittest.TestCase):
    def test_init_valid(self):
        """
        Test a valid constructor of AddRemoveHelper
        """

        try:
            _ = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'add')
        except ValueError:
            self.assertTrue(False)

    def test_init_invalid(self):
        """
        Test invalid constructors of AddRemoveHelper
        """
        instances = [
            partial_class((0.5, "add")),  # build_config is a float
            partial_class((DEFAULT_BUILD_CONFIG, 0.5)) # command is a float
        ]

        for instance in instances:
            try:
                instance()
            except ValueError:
                pass
            else:
                self.assertTrue(False)

    def test_search(self)
