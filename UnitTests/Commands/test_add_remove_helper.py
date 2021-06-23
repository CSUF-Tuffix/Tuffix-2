#!/usr/bin/env python3.9

from Tuffix.Commands import AddRemoveHelper, AbstractCommand
from Tuffix.Keywords import AbstractKeyword
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest
import functools
import textwrap
import json
import pathlib


def partial_class(container: tuple):
    # NOTE : please include this in all derived classes
    # Duplicate code

    build_config, name = container
    body = {
        "__init__": functools.partialmethod(
            AddRemoveHelper.__init__,
            build_config=build_config,
            command=name
        )
    }
    return type("test", (AddRemoveHelper, ), body)


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
            partial_class((DEFAULT_BUILD_CONFIG, 0.5))  # command is a float
        ]

        for instance in instances:
            try:
                instance()
            except ValueError:
                pass
            else:
                self.assertTrue(False)

    def test_search_success(self):
        """
        Test the search function for installed custom keywords (the file should be found)
        """

        payload = {
            "name": "osc",
            "instructor": "William McCarthy",
            "packages": ["cowsay", "vim"]
        }

        payload_path = pathlib.Path("/var/lib/tuffix/json_payloads/osc.json")

        with open(payload_path, "w") as fp:
            json.dump(payload, fp)

        helper = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'searcher')
        resultant = helper.search('osc')
        self.assertTrue(isinstance(resultant, tuple))
        status, class_instance = resultant
        self.assertTrue(
            isinstance(status, bool) and
            (status == True) and
            isinstance(class_instance, AbstractKeyword)
        )
        payload_path.unlink()

    def test_search_fail(self):
        """
        Test the search function for installed custom keywords (the file should not be found)
        """

        helper = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'searcher')
        resultant = helper.search('jareddyreson')
        self.assertTrue(isinstance(resultant, tuple))
        status, class_instance = resultant
        self.assertTrue(
            isinstance(status, bool) and
            (status == False) and
            isinstance(class_instance, type(None))
        )
