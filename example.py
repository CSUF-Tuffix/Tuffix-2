#!/usr/bin/env python3.9

from Tuffix.Driver import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
from Tuffix.Exceptions import *

import unittest
import importlib.util

tests = {
    "DriverTest": "UnitTests/test_tuffix_driver.py",
    # "lsb_parser": "UnitTests/test_lsb_parser.py",
    # "status": "UnitTests/test_status.py",
    # NOTE: Unknown how to test -> "sudo_run": "UnitTests/test_sudo_run.py"
    # "utility": "UnitTests/test_utility_functions.py"
}

runner = unittest.TextTestRunner()

for name, path in tests.items():
    print(f'\t-  [TEST] Conducting {name}')
    spec = importlib.util.spec_from_file_location("test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _test = getattr(module, name, None)
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(_test)
    # runner.run(test_suite)
