#!/usr/bin/env python3.9

from Tuffix.Driver import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
import unittest
from Tuffix.Editors import Editors
from Tuffix.Exceptions import *

class EditorTest(unittest.TestCase):
    def test_prompt(self):
        editor_ = Editors()
        # editor_.prompt() # requires manual entry
        editor_.prompt((True, 0)) # proceed without user input
        try:
            editor_.prompt((True, 85)) # proceed without user input (incorrect selection)
        except UsageError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        editor_.emacs()

if __name__ == '__main__':
    unittest.main()
