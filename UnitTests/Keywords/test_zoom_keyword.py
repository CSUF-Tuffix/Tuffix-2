from Tuffix.Keywords import ZoomKeyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, State, read_state
from Tuffix.Commands import InitCommand

import unittest


class ZoomKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.Zoom = ZoomKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        self.Zoom.add()
        self.assertTrue(self.Zoom.is_deb_package_installed('zoom'))

    def test_remove(self):
        self.Zoom.remove()
        self.assertFalse(self.Zoom.is_deb_package_installed('zoom'))
