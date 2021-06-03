#!/usr/bin/env python3.9

from Tuffix.Driver import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
import unittest


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

    def test_remove(self):
        command = "tuffix remove test"
        main(command.split())

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

if __name__ == '__main__':
    unittest.main()
