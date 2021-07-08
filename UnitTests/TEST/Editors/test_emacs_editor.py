from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State, BuildConfig
from Tuffix.Editors import EditorBaseKeyword, EmacsKeyword
from Tuffix.SudoRun import SudoRun

import unittest


class TestEditorGeneric(unittest.TestCase):
    @classmethod
    def setUpClass(cls, instance: EditorBaseKeyword):
        if not(issubclass(type(instance), EditorBaseKeyword) and
               issubclass(type(instance), AbstractKeyword)):
            raise ValueError(f'expecting subclass of `EditorBaseKeyword`')

        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.keyword = instance

        self.assertTrue(
            hasattr(cls.keyword, 'build_config') and
            hasattr(cls.keyword, 'executor')
        )
        self.assertTrue(
            isinstance(cls.keyword.build_config, BuildConfig) and
            isinstance(cls.keyword.executor, SudoRun)
        )

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    @classmethod
    def generic_check_add(self):

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue(self.keyword.name not in before_install.editors)
        self.Emacs.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue(self.keyword.name in after_install.editors)

        try:
            self.assertTrue(self.keyword.is_deb_package_installed(self.name))
        except EnvironmentError:
            self.assertTrue(False)

    @classmethod
    def generic_check_remove(self):
        self.keyword.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue(self.keyword.name not in after_removal.editors)

        try:
            self.assertFalse(self.keyword.is_deb_package_installed(self.name))
        except EnvironmentError:
            self.assertTrue(False)


class EmacsKeywordTest(unittest.TestCase):
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
