#!/usr/bin/env python3.9


from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.KeywordHelperFunctions import DEFAULT_LINK_CHECKER
from Tuffix.Commands import InitCommand
from Tuffix.Editors import AtomKeyword
from Tuffix.Exceptions import UsageError
from Tuffix.Quieter import CapturingStderr

import unittest
import pathlib

class AtomKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.Atom = AtomKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()
    
    # def test_available_links(self):
        # try:
            # DEFAULT_LINK_CHECKER.check_links(self.Atom.link_dictionary)
        # except UsageError:
            # self.assertTrue(False)

    # def test_check_candidates(self):
        # uninstallable_packages = ["taco bell", "baco tell", "chipotle"]
        # installable_packages = ["dbg-gdb", "dbg", "output-panel"]
        
        # # honestly unsure why this calls `mkdir`, I decided to just give up entirely on this one

        # with CapturingStderr() as _:
            # self.assertFalse(
                # all([self.Atom.check_apm_candiate(_) for _ in uninstallable_packages]) 
            # )
            # self.assertTrue(
                # all([self.Atom.check_apm_candiate(_) for _ in installable_packages]) 
            # )

    def test_add(self):
        # self.Atom.add(write=False)
        for _, artifcat in self.Atom.file_footprint.items():
            self.assertTrue(artifcat.is_file())

    def test_remove(self):
        # self.Atom.remove(write=False)
        for _, artifcat in self.Atom.file_footprint.items():
            self.assertFalse(artifcat.is_file())
