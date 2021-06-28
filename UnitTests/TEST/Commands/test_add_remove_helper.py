#!/usr/bin/env python3.9

from Tuffix.Commands import AddRemoveHelper, AbstractCommand
from Tuffix.Keywords import AbstractKeyword, AllKeyword, TMuxKeyword
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG, read_state
from Tuffix.Exceptions import *

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

    def test_rewrite_state_install(self):
        """
        Test if the program can update the state
        """

        original_state = read_state(DEFAULT_BUILD_CONFIG)

        helper = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'rewriter')
        example_keyword = TMuxKeyword(DEFAULT_BUILD_CONFIG)

        helper.rewrite_state(keyword=example_keyword,
                             install=True)  # install the keyword

        updated_state = read_state(DEFAULT_BUILD_CONFIG)  # note the state

        helper.rewrite_state(keyword=example_keyword,
                             install=False)  # remove the keyword

        reverted_state = read_state(
            DEFAULT_BUILD_CONFIG)  # note the state again

        # check if the new state is equal to the snap shot
        self.assertTrue(original_state == reverted_state)

        """
        match read_state(DEFAULT_BUILD_CONFIG):
            case {"version": version, "installed": keywords_installed, "editors": editors_installed}:;
                if(installed)
            case _:
                self.assertTrue(False)
        """
    
    def test_run_commands_install(self):
        helper_add = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'add')
        # Test install
        helper_add.run_commands(container=[(True, TMuxKeyword(DEFAULT_BUILD_CONFIG))], install=True)
        updated_state = read_state(DEFAULT_BUILD_CONFIG)  # note the state
        self.assertTrue("tmux" in updated_state.installed)

        # Test reinstall
        try:
            helper_add.run_commands(container=[(True, TMuxKeyword(DEFAULT_BUILD_CONFIG))], install=True)
        except UsageError:
            pass
        else:
            self.assertTrue(False)

    def test_run_commands_remove(self):
        helper_remove = AddRemoveHelper(DEFAULT_BUILD_CONFIG, 'remove')
        # Test Remove
        helper_remove.run_commands(container=[(True, TMuxKeyword(DEFAULT_BUILD_CONFIG))], install=False)
        updated_state= read_state(DEFAULT_BUILD_CONFIG)
        self.assertTrue("tmux" not in updated_state.installed)

        try:
            helper_remove.run_commands([(True, AllKeyword(DEFAULT_BUILD_CONFIG))], install=False)
        except UsageError:
            pass
        else:
            self.assertTrue(False)

    def test_run_commands_invalid(self):
        helper_invalid = AddRemoveHelper(DEFAULT_BUILD_CONFIG, '__remove')
        try:
            helper_invalid.run_commands(container=[(True, TMuxKeyword(DEFAULT_BUILD_CONFIG))], install=True)
        except AttributeError:
            pass
        else:
            self.assertTrue(False)
