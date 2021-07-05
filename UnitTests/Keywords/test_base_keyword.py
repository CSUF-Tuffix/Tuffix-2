from Tuffix.Keywords import BaseKeyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

import unittest

class TestBaseKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Base = BaseKeyword(DEBUG_BUILD_CONFIG)

    def test_add(self):
        # this is without building googletest and googlemock from scratch
        # self.Base.add()
        self.Base.google_test_build()
        self.Base.google_test_attempt()
