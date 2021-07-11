from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Editors import GeanyKeyword


class GeanyKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(GeanyKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Install geany and check the state path
        """

        self.generic_check_add()

    def test_remove(self):
        """
        Remove geany and check the state path
        """

        self.generic_check_remove()
