from Tuffix.Keywords import ClangKeyword
from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from UnitTests.Base import TestEditorGeneric as TestKeywordGeneric

import shutil
import unittest
import os
import subprocess


class TestClangKeywordTest(TestKeywordGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(ClangKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Test to see if we can install all dependencies
        """
        self.generic_check_add()

    def test_remove(self):
        """
        We are only interested in removing mention of
        the keyword. Most of these installation candiates
        are critical for most software development
        outside of academic work
        """

        self.generic_check_remove()
