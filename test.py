#!/usr/bin/env python3.9

import UnitTests
from pprint import pprint as pp
import unittest

print("[INFO] Running Tuffx Unit Tests...")

runner = unittest.TextTestRunner()

for test, _class in UnitTests.__unit_test_hierarchy__.items():
    print(f'\t- [TEST] Conducting {test}')

    try:
        _test = getattr(UnitTests, test, None)
        _class_instance = getattr(_test, _class)

        test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(
            _class_instance)
        runner.run(test_suite)
    except AttributeError as e:
        print(
            f'[INTERNAL ERROR] Could not load {test}, does not appear to be a member of UnitTests')
        quit()
    """
    tests = {
        # each test module name

        "test_lsb_parser": {
            # Actual Test Conglomorate Conducted
            "LSBTest": {
                # each test actually conducted
                "test_constructor": [False, function_pointer()]
            }
        }
    }
    """

"""
Example log file:

[INFO] Running Tuffx Unit Tests...

[TEST 0: test_lsb_parser] Conducting....

    - [TEST 0.0: test_constructor] - PASS
    - [TEST 0.1: test_example_made_up] - FAIL

[ERROR] Halting execution of unit tests,  failure at [TEST NAME]

"""
