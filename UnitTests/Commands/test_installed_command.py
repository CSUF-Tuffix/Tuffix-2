#!/usr/bin/env python3.9

from Tuffix.Commands import AddCommand, RemoveCommand, InitCommand, InstalledCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state

from Tuffix.Keywords import KeywordContainer

from Tuffix.Quieter import Capturing

import unittest
import textwrap


class InstalledCommandTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init = InitCommand(DEBUG_BUILD_CONFIG)
        init.create_state_directory()
        cls.installed_command = InstalledCommand(DEBUG_BUILD_CONFIG)
        cls.installed_packages = ["tmux"]

    def test_installed_target_not_present(self):
        """
        When there are no keywords installed
        currently on the machine
        """

        with Capturing() as output:
            self.installed_command.execute([])
        self.assertTrue(
            output == ['[INFO] No keywords are installed']
        )

    def test_installed_target_present(self):
        """
        Install a package and consult the output
        """

        __add = AddCommand(DEBUG_BUILD_CONFIG)
        __add.execute(self.installed_packages)
        with Capturing() as output:
            self.installed_command.execute([])
        message = """
        [INFO] Tuffix installed keywords (1):
        tmux
        """
        self.assertTrue(
            output == [textwrap.dedent(message).strip()]
        )

    def test_installed_target_present_removed(self):
        """
        Remove currently installed package
        and test if there is any output
        """

        __remove = RemoveCommand(DEBUG_BUILD_CONFIG)
        __remove.execute(self.installed_packages)
        self.assertTrue(
            self.test_installed_target_not_present()
        )
