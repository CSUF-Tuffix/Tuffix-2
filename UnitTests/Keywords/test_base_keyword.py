from Tuffix.Keywords import BaseKeyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, State, read_state
from Tuffix.Commands import InitCommand

import unittest

class TestBaseKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Base = BaseKeyword(DEBUG_BUILD_CONFIG)

    def test_add(self):
        self.Base.add()
        self.assertTrue(self.Base.google_test_attempt())
