#!/usr/bin/env python3.9

from Tuffix.Driver import *
import unittest


class DriverTest(unittest.TestCase):

    def test_init(self):
        command = "tuffix init"
        main(command.split())
    def test_remove(self):
        command = "tuffix add base"
        main(command.split())
