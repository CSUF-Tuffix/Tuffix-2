from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Editors import EmacsKeyword


class EmacsKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(EmacsKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Install emacs and check the state path
        """

        self.generic_check_add()

    def test_remove(self):
        """
        Remove emacs and check the state path
        """

        self.generic_check_remove()
