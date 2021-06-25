#!/usr/bin/env python3.9

from Tuffix.Commands import StatusCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

from Tuffix.Quieter import Capturing

import unittest
import termcolor


class StatusCommandTest(unittest.TestCase):
    """
    NOTE: is incomplete
    """
    @classmethod
    def setUpClass(cls):
        cls.status_command = StatusCommand(DEBUG_BUILD_CONFIG)

    def test_success(self):
        message = f'{"#" * 10} [INFO] Status succeeded {"#" * 10}'

        with Capturing() as output:
            self.status_command.execute([])
        self.assertTrue(
            termcolor.colored(message, "green") == output[-1]
        )
