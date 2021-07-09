#!/usr/bin/env python3

from Tuffix.UnitTestOrchestrator import TuffixTestRunner
import pathlib

R = TuffixTestRunner(
    parent_dir=pathlib.Path("UnitTests/"),
    pedantic=True
)
# R.test_certain_class("AbstractKeyword")
R.run_all_tests()
