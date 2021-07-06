#!/usr/bin/env python3.9

from Tuffix.Commands import ListCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

from Tuffix.Quieter import Capturing

import unittest


class ListCommandTest(unittest.TestCase):
    def test_list(self):
        """
        Ensure there is output from this command
        """

        __list = ListCommand(DEBUG_BUILD_CONFIG)
        with Capturing() as output:
            __list.execute([])
        self.assertTrue(
            (argc  := (len(output)) > 0)
        )
