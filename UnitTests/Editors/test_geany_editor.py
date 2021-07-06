from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import GeanyKeyword

import unittest

IGNORE_ME = True


class GeanyKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()
        cls.Geany = GeanyKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        """
        Install geany and check the state path
        """

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("geany" not in before_install.editors)
        self.Geany.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("geany" in after_install.editors)

        try:
            self.assertTrue(self.Geany.is_deb_package_installed('geany'))
        except EnvironmentError:
            self.assertTrue(False)

    def test_remove(self):
        """
        Remove geany and check the state path
        """

        self.Geany.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("geany" not in after_removal.editors)

        try:
            self.assertFalse(self.Geany.is_deb_package_installed('geany'))
        except EnvironmentError:
            self.assertTrue(False)
