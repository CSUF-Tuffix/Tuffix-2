#!/usr/bin/env python3.9

from Tuffix.Driver import *
import unittest


class DriverTest(unittest.TestCase):

    def test_init(self):
        command = "tuffix init"
        main(command.split())

    def test_add(self):
        command = "tuffix add base"
        main(command.split())

    # def test_remove(self):
        # command = "tuffix remove base"
        # main(command.split())

    # def test_list(self):
        # command = "tuffix list"
        # main(command.split())

    # def test_installed(self):
        # command = "tuffix installed"
        # main(command.split())

    # def test_status(self):
        # command = "tuffix status"
        # main(command.split())

    # def test_custom(self):
        # command = "tuffix custom /tmp/example.json"
        # main(command.split())
