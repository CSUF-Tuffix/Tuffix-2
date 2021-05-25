#!/usr/bin/env python3.9

from Tuffix.Driver import *
import unittest


class DriverTest(unittest.TestCase):

    def test_init(self):
        main(["tuffix", "init"])
