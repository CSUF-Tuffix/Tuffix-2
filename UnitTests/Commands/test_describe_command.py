#!/usr/bin/env python3.9

from Tuffix.Keywords import KeywordContainer
from Tuffix.Commands import DescribeCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

from Tuffix.Quieter import Capturing

import unittest


class DescribeCommandTest(unittest.TestCase):
    def test_describe_command_valid(self):
        container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        describe = DescribeCommand(DEFAULT_BUILD_CONFIG)
        for keyword in container.container:
            with Capturing() as output:
                name, description = keyword.name, keyword.description
                describe(name)
            self.assertTrue([f'{name}: {description}'] == output)
