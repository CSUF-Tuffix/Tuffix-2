from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Editors import EclipseKeyword


class EclipseKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(EclipseKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_add(self):
        """
        Install eclipse and check the state path
        """

        self.generic_check_add()

    def test_remove(self):
        """
        Remove eclipse and check the state path
        """

        self.generic_check_remove()
