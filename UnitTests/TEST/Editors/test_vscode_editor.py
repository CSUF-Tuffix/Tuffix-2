from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import VscodeKeyword

import unittest

IGNORE_ME = True

class VscodeKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()
        cls.Vscode = VscodeKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        """
        Install vscode and check the state path
        """

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("code" not in before_install.editors)
        self.Vscode.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("code" in after_install.editors)

    def test_remove(self):
        """
        Remove vscode and check the state path
        """

        self.Vscode.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("code" not in after_removal.editors)

