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

choices = [x for x in os.listdir(
    parent_dir) if (os.path.isdir(f'{parent_dir}{x}') and x not in R.excluded_dirs)]

pedantic = arguments.pedantic

if((test := arguments.test)):
    if(test not in choices):
        print("hey this test was not valid")
    else:
        valid_tests = test.split(",")
        for valid_test in valid_test:
            # R.test_certain_class(valid_test)

if(arguments.all):
    print("conducting all tests")
    # R.run_all_tests()
