from Tuffix.Keywords import BaseKeyword
from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from UnitTests.BaseEditorTest import TestEditorGeneric as TestKeywordGeneric

import shutil
import unittest

class TestBaseKeywordTest(TestKeywordGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(BaseKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def google_generic(self) -> bool:
        """
        Goal: small test to check if Google Test works after install
        TODO: change link to be under CSUF domain
        TEST_URL = "https://github.com/JaredDyreson/tuffix-google-test.git"
        """

        TEST_URL = self.Base.link_dictionary["TEST_URL"].link
        TEST_DEST = "test"

        os.chdir("/tmp")
        if(os.path.isdir(TEST_DEST)):
            shutil.rmtree(TEST_DEST)
        subprocess.run(['git', 'clone', TEST_URL, TEST_DEST])
        os.chdir(TEST_DEST)
        subprocess.check_output(['clang++', '-v', 'main.cpp', '-o', 'main'])
        self.assertTrue(
            (output := subprocess.run(['make', 'all']).returncode) != 0
        )

    def test_add(self):
        """
        Test to see if we can install all dependencies
        """
        self.generic_check_add()
        self.google_generic()

    def test_remove(self):
        """
        Test to see if we can remove all dependencies
        NOTE: we have no way of removing the manually compiled googletest
        """

        self.generic_check_remove()
