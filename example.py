#!/usr/bin/env python3.9

from Tuffix.Driver import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
import unittest
from Tuffix.Editors import Editors
from Tuffix.Exceptions import *

# class EditorTest(unittest.TestCase):
    # def test_prompt(self):
        # editor_ = Editors()
        # # editor_.prompt() # requires manual entry
        # editor_.prompt((True, 0)) # proceed without user input
        # try:
            # editor_.prompt((True, 85)) # proceed without user input (incorrect selection)
        # except UsageError:
            # self.assertTrue(True)
        # else:
            # self.assertTrue(False)


class DriverTest(unittest.TestCase):

   # All commented out ones do work (except for Custom)

    # def test_init(self):
        # command = "tuffix init"
        # main(command.split())

    # def test_list(self):
        # command = "tuffix list"
        # main(command.split())

    # def test_add(self):
        # command = "tuffix add test"
        # main(command.split())

    # def test_remove(self):
        # command = "tuffix remove test"
        # main(command.split())

    # def test_installed(self):
        # command = "tuffix installed"
        # main(command.split())

    # def test_status(self):
        # command = "tuffix status"
        # main(command.split())

    # def test_custom(self):
        # command = "tuffix custom json_payload/OSC.json"
        # main(command.split())

    # def test_describe(self):
        # k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        # for keyword in k_container.container:
            # command = f'tuffix describe {keyword.name}'
            # main(command.split())

    def test_sysupgrade(self):
        command = "tuffix add supgrade"
        main(command.split())
if __name__ == '__main__':
    unittest.main()
