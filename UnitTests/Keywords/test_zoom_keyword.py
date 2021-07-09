from Tuffix.Keywords import ZoomKeyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from UnitTests.BaseEditorTest import TestEditorGeneric as TestKeywordGeneric

import unittest

class ZoomKeywordTest(TestKeywordGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(ZoomKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_candidates(self):
        self.generic_check_available_candidates()

    def test_add(self):
        """
        Install zoom and check the state path
        """

        self.generic_check_add()

    def test_remove(self):
        """
        Remove zoom and check the state path
        """

        self.generic_check_remove()
