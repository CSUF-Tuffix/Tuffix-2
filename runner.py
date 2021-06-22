#!/usr/bin/env python3.9

from Tuffix.Driver import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
from Tuffix.Exceptions import *
from Tuffix.Quieter import quiet
from UnitTests.SequentialTest import SequentialTestLoader

import unittest
import importlib.util

"""
format:

"<CLASS NAME OF TEST>": ["PATH", SILENT(False)/VERBOSE(True)]
"""

tests = {
    "AbstractKeywordTest": ["UnitTests/test_abstract_keyword.py", False]
    #"KeywordTest": ["UnitTests/test_keywords.py", True],
    # "DriverTest": ["UnitTests/test_tuffix_driver.py", False],
    #"UtilityFunctionTest": ["UnitTests/test_utility_functions.py", False],
    #"LSBTest": ["UnitTests/test_lsb_parser.py", False],
    #"StatusTest": ["UnitTests/test_status.py", False]
    # NOTE: Unknown how to test -> "sudo_run": "UnitTests/test_sudo_run.py"
}

runner = unittest.TextTestRunner()

for name, arguments in tests.items():
    path, pedantic = arguments
    print(f'  - [TEST] Conducting {name}')
    spec = importlib.util.spec_from_file_location("test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _test = getattr(module, name, None)
    test_suite = SequentialTestLoader().loadTestsFromTestCase(_test)
    if(pedantic):
        runner.run(test_suite)
    else:
        with quiet():
            runner.run(test_suite)
