from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.Commands import InitCommand
from Tuffix.Configuration import read_state, State
from Tuffix.Editors import EditorBaseKeyword
from Tuffix.Exceptions import UsageError
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER

import unittest

"""
Unit test desgined to encapsulate all EditorKeywords
This is the parent classes of all tests in UnitTests/Editors
"""


class TestEditorGeneric(unittest.TestCase):
    @classmethod
    def setUpClass(cls, instance: EditorBaseKeyword):
        if not(issubclass(type(instance), EditorBaseKeyword) or
               issubclass(type(instance), AbstractKeyword)):
            raise ValueError(
                f'expecting subclass of `EditorBaseKeyword` or `AbstractKeyword`')

        cls.state = State(instance.build_config,
                          instance.build_config.version,
                          [], [])
        cls.Init = InitCommand(instance.build_config)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.keyword = instance

        _type = type(cls.keyword)
        if(issubclass(_type, AbstractKeyword) and
           not issubclass(_type, EditorBaseKeyword)):
            cls.correct_attr = (True, False) # 0: regular keyword, 1: editorkeyword
        else:
            cls.correct_attr = (False, True)

        cls.generic_check_available_candidates()
        cls.generic_check_links()

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    @classmethod
    def generic_check_available_candidates(self):
        """
        See if all of the checkable packages can be installed
        """

        if(hasattr(self.keyword, 'checkable_packages')):
            try:
                self.keyword.check_candiates()
            except KeyError:
                self.assertTrue(False)

    def obtain_correct_attribute(self, state: State):
        regular_keyword, editor = self.correct_attr
        if(regular_keyword):
            return getattr(state, 'installed')
        return getattr(state, 'editors')

    def generic_check_add(self):
        """
        Ensure the keyword installs properly
        """

        before_install = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name not in self.obtain_correct_attribute(before_install))
        self.keyword.add()
        after_install = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name in self.obtain_correct_attribute(after_install))

        try:
            self.assertTrue(
                all([self.keyword.is_deb_package_installed(pkg) for pkg in self.keyword.packages]))
        except EnvironmentError:
                self.assertTrue(False)

    def generic_check_remove(self):
        """
        Ensure the keyword is removed properly
        """

        self.keyword.remove()
        after_removal = read_state(self.keyword.build_config)
        self.assertTrue(
            self.keyword.name not in self.obtain_correct_attribute(after_removal))

        try:
            self.assertTrue(
                self.keyword.is_deb_package_installed(self.keyword.name) or
                all([self.keyword.is_deb_package_installed(pkg) for pkg in self.keyword.packages]))
        except EnvironmentError:
            self.assertTrue(False)

        if(hasattr(self.keyword, 'file_footprint')):
            for _, artifcat in self.keywords.file_footprint.items():
                self.assertFalse(artifcat.is_file())

    @classmethod
    def generic_check_links(self):
        """
        Check if the links associated with
        the keyword are up (external dependencies)
        """

        if(hasattr(self.keyword, 'link_dictionary')):
            try:
                DEFAULT_LINK_CHECKER.check_links(self.keyword.link_dictionary)
            except UsageError:
                self.assertTrue(False)
