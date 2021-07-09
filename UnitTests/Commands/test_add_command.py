from Tuffix.Commands import AddCommand, AbstractCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest


class AddCommandTest(unittest.TestCase):
    # NOTE: this test has been done in Commands/test_add_remove_helper.py
    def test_init(self):
        try:
            AddCommand(DEFAULT_BUILD_CONFIG)
        except ValueError:
            self.assertTrue(False)
