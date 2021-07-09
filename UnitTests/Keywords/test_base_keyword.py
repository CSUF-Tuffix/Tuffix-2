from Tuffix.Keywords import BaseKeyword
from Tuffix.Commands import InitCommand
from UnitTests.BaseEditorTest import TestBaseKeywordTest

import shutil
import unittest

IGNORE_ME = True


class TestBaseKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.Base = BaseKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def google_test_attempt(self) -> bool:
        """
        Goal: small test to check if Google Test works after install
        TODO: change link to be under CSUF domain
        TEST_URL = "https://github.com/JaredDyreson/tuffix-google-test.git"
        """

        TEST_URL = self.Base.link_dictionary["TEST_URL"].link
        TEST_DEST = "test"

        os.chdir("/tmp")
        if(os.path.isdir(TEST_DEST)):
            shutil.rmtree(TEST_DEST)
        subprocess.run(['git', 'clone', TEST_URL, TEST_DEST])
        os.chdir(TEST_DEST)
        subprocess.check_output(['clang++', '-v', 'main.cpp', '-o', 'main'])
        ret_code = subprocess.run(['make', 'all']).returncode
        if(ret_code != 0):
            print(colored("[ERROR] Google Unit test failed!", "red"))
        else:
            print(colored("[SUCCESS] Google unit test succeeded!", "green"))

        return (ret_code != 0)

    def test_add(self):
        """
        Test to see if we can install all dependencies
        """

        self.Base.add()
        self.assertTrue(self.google_test_attempt())  # did it build correctly
        current_state = read_state(DEBUG_BUILD_CONFIG)
        # is atom currently installed in the state
        self.assertTrue(
            "atom" in current_state.editors
        )
        self.assertTrue((atom := shutil.which("atom")))

    def test_remove(self):
        """
        Test to see if we can remove all dependencies
        NOTE: we have no way of removing the manually compiled googletest
        """

        self.Base.remove()
        current_state = read_state(DEBUG_BUILD_CONFIG)
        # is atom currently installed in the state
        self.assertTrue(
            "atom" not in current_state.editors
        )
        self.assertFalse((atom := shutil.which("atom")))
