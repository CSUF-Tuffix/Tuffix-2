#!/usr/bin/env python3.9

from Tuffix.Keywords import KeywordContainer
from Tuffix.Editors import EditorKeywordContainer, EditorBaseKeyword
from Tuffix.Commands import DescribeCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG, read_state

from Tuffix.Quieter import Capturing

import unittest


class DescribeCommandTest(unittest.TestCase):
    def test_describe_command_valid(self):
        """
        List all valid commands and check the output
        of the function call
        Custom keywords are NOT CURRENTLY SUPPORTED
        """

        container = KeywordContainer(DEFAULT_BUILD_CONFIG).container
        container.extend(EditorKeywordContainer(
            DEFAULT_BUILD_CONFIG).container)

        describe = DescribeCommand(DEFAULT_BUILD_CONFIG)
        for keyword in container:
            with Capturing() as output:
                name, description = keyword.name, keyword.description
                describe.execute([name])
            self.assertTrue([f'{name}: {description}'] == output)
