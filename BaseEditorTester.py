"""
All the unit tests for these editors are following the
same style, it would be nice to just inherit from one parent class

NOTE:

this is heavily broken and I don't know why
I spent way too much time trying to get this to work
and wasted valuable time
"""

from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import EditorBaseKeyword

import unittest


class BaseTestClass:
    class BaseEditorsTest(unittest.TestCase):
        @classmethod
        def setUp(cls):
            cls.state = State(DEBUG_BUILD_CONFIG,
                              DEBUG_BUILD_CONFIG.version,
                              [], [])
            cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
            cls.Init.create_state_directory()
            cls.Keyword = None
            cls.state.write()

        def test_add(self):
            """
            Install editor and check the state path
            """

            before_install = read_state(DEBUG_BUILD_CONFIG)
            self.assertTrue(self.Keyword.name not in before_install.editors)
            self.Keyword.add()
            after_install = read_state(DEBUG_BUILD_CONFIG)
            self.assertTrue(self.Keyword.name in after_install.editors)

            try:
                self.assertTrue(
                    self.Keyword.is_deb_package_installed(self.Keyword.name))
            except EnvironmentError:
                self.assertTrue(False)

        def test_remove(self):
            """
            Remove editor and check the state path
            """

            self.Keyword.remove()
            after_removal = read_state(DEBUG_BUILD_CONFIG)
            self.assertTrue(self.Keyword.name not in after_removal.editors)

            try:
                self.assertFalse(
                    self.Keyword.is_deb_package_installed(self.Keyword.name))
            except EnvironmentError:
                self.assertTrue(False)


# class SubTest(BaseTestClass.BaseEditorKeyword):
    # @classmethod
    # def setUpClass(cls):
        # super(BaseTestClass.CommonTests, cls).setUpClass()
        # cls.Keyword = 'EXAMPLE'

    # def test_example(self):
        # self.assertTrue(hasattr(self, 'name'))
        # self.assertTrue(hasattr(self, 'keyword'))
