from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Editors import VimKeyword

import unittest

class VimKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(VimKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Install vim and check the state path
        """

        self.generic_check_add()

    @unittest.skip("vim is my editor")
    def test_remove(self):
        """
        Remove vim and check the state path
        """

        self.generic_check_remove()
