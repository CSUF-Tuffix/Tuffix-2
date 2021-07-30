from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state
from Tuffix.Editors import EclipseKeyword

import unittest


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

        before_install = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name not in self.obtain_correct_attribute(before_install))
        self.keyword.add()
        after_install = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name in self.obtain_correct_attribute(after_install))

    def test_remove(self):
        """
        Remove eclipse and check the state path
        """

        self.keyword.remove()
        after_removal = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name not in self.obtain_correct_attribute(after_removal))
