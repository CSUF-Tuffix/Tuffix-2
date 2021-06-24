#!/usr/bin/env python3.9

from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest


class InitCommandTest(unittest.TestCase):
    def test_create_state_directory(self):
        """
        Test if the state directory can be created
        """

        init = InitCommand(DEFAULT_BUILD_CONFIG)
        init.create_state_directory()
