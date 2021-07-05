from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import EclipseKeyword

import unittest

IGNORE_ME = True


class EclipseKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()
        cls.Eclipse = EclipseKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        """
        Install eclipse and check the state path
        """

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("eclipse" not in before_install.editors)
        self.Eclipse.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("eclipse" in after_install.editors)
        for name, path in self.Eclipse.file_footprint.items():
            self.assertTrue(path.is_file())

    def test_remove(self):
        """
        Remove eclipse and check the state path
        """

        self.Eclipse.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("eclipse" not in after_removal.editors)
        for name, path in self.Eclipse.file_footprint.items():
            self.assertFalse(path.is_file())
