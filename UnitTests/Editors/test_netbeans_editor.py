from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import NetbeansKeyword

import unittest

IGNORE_ME = True


class NetbeansKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()
        cls.Netbeans = NetbeansKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        """
        Install netbeans and check the state path
        """

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("netbeans" not in before_install.editors)
        self.Netbeans.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("netbeans" in after_install.editors)

        try:
            self.assertTrue(self.Netbeans.is_deb_package_installed('netbeans'))
        except EnvironmentError:
            self.assertTrue(False)

    def test_remove(self):
        """
        Remove netbeans and check the state path
        """

        self.Netbeans.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("netbeans" not in after_removal.editors)

        try:
            self.assertFalse(
                self.Netbeans.is_deb_package_installed('netbeans'))
        except EnvironmentError:
            self.assertTrue(False)
