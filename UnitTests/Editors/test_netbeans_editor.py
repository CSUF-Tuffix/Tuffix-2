from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Editors import NetbeansKeyword

class NetbeansKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(NetbeansKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Install netbeans and check the state path
        """

        self.generic_check_add()

    def test_remove(self):
        """
        Remove netbeans and check the state path
        """

        self.generic_check_remove()
