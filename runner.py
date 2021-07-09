#!/usr/bin/env python3

from Tuffix.UnitTestOrchestrator import TuffixTestRunner

import argparse
import pathlib
import os

"""
Argument parser
"""

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--all",
                    help="test all components", action="store_true")

parser.add_argument("-p", "--pedantic",
                    help="allow for output of tests to be pedantic", action="store_true")
parser.add_argument("-t", "--test",
                    help="test certain components, comma separated", type=str)

arguments = parser.parse_args()

R = TuffixTestRunner(
    parent_dir=pathlib.Path("UnitTests/"),
    pedantic=True
)

pedantic = arguments.pedantic

if((test := arguments.test)):
    for valid_test in test.split(","):
        R.test_certain_class(valid_test)

if(arguments.all):
    R.run_all_tests()
