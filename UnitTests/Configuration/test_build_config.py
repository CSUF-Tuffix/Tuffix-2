#!/usr/bin/env python3.9

from Tuffix.Configuration import BuildConfig, DEFAULT_BUILD_CONFIG, DEBUG_BUILD_CONFIG

# this by default will test the constructor

import unittest


class BuildConfigTest(unittest.TestCase):
    def test_eq_operator(self):
        self.assertFalse(DEFAULT_BUILD_CONFIG == DEBUG_BUILD_CONFIG)
