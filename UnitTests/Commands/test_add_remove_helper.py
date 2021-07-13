#!/usr/bin/env python3.9

from Tuffix.Commands import AddRemoveHelper, AbstractCommand, InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Exceptions import UsageError
from Tuffix.Keywords import AbstractKeyword, AllKeyword, TMuxKeyword

import functools
import json
import pathlib
import textwrap
import unittest


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
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_init_valid(self):
        """
        Test a valid constructor of AddRemoveHelper
        """

        try:
            _ = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'add')
        except ValueError:
            self.assertTrue(False)

    def test_init_invalid(self):
        """
        Test invalid constructors of AddRemoveHelper
        """
        instances = [
            partial_class((0.5, "add")),  # build_config is a float
            partial_class((DEBUG_BUILD_CONFIG, 0.5))  # command is a float
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

        helper = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'searcher')
        resultant = helper.search('osc')
        self.assertTrue(isinstance(resultant, tuple))
        status, class_instance = resultant
        self.assertTrue(
            isinstance(status, bool) and
            (status) and
            isinstance(class_instance, AbstractKeyword)
        )
        payload_path.unlink()

    def test_search_fail(self):
        """
        Test the search function for installed custom keywords (the file should not be found)
        """

        helper = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'searcher')
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

        original_state = read_state(DEBUG_BUILD_CONFIG)

        helper = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'rewriter')
        example_keyword = TMuxKeyword(DEBUG_BUILD_CONFIG)

        helper.rewrite_state(keyword=example_keyword,
                             install=True)  # install the keyword

        updated_state = read_state(DEBUG_BUILD_CONFIG)  # note the state

        helper.rewrite_state(keyword=example_keyword,
                             install=False)  # remove the keyword

        reverted_state = read_state(
            DEBUG_BUILD_CONFIG)  # note the state again

        # check if the new state is equal to the snap shot
        self.assertTrue(original_state == reverted_state)

        """
        match read_state(DEBUG_BUILD_CONFIG):
            case {"version": version, "installed": keywords_installed, "editors": editors_installed}:;
                if(installed)
            case _:
                self.assertTrue(False)
        """

    def test_run_commands_install(self):
        helper_add = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'add')
        # Test install
        helper_add.run_commands(
            container=[
                (True, TMuxKeyword(DEBUG_BUILD_CONFIG))], install=True)
        updated_state = read_state(DEBUG_BUILD_CONFIG)  # note the state
        self.assertTrue("tmux" in updated_state.installed)

        # Test reinstall
        try:
            helper_add.run_commands(
                container=[
                    (True, TMuxKeyword(DEBUG_BUILD_CONFIG))], install=True)
        except UsageError:
            pass
        else:
            self.assertTrue(False)

    def test_run_commands_remove(self):
        helper_remove = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'remove')
        # Test Remove
        helper_remove.run_commands(
            container=[
                (True, TMuxKeyword(DEBUG_BUILD_CONFIG))], install=False)
        updated_state = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("tmux" not in updated_state.installed)

        try:
            helper_remove.run_commands(
                [(True, AllKeyword(DEBUG_BUILD_CONFIG))], install=False)
        except UsageError:
            pass
        else:
            self.assertTrue(False)

    def test_run_commands_invalid(self):
        helper_invalid = AddRemoveHelper(DEBUG_BUILD_CONFIG, '__remove')
        try:
            helper_invalid.run_commands(
                container=[
                    (True, TMuxKeyword(DEBUG_BUILD_CONFIG))], install=True)
        except AttributeError:
            pass
        else:
            self.assertTrue(False)
