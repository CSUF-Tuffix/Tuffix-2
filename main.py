#!/usr/bin/env python3.9

"""
New arg parser for Tuffix

TODO:

- add
- remove
- list

"""

# System Imports
import argparse
import os
import sys
import unittest

# Tuffix Defined Imports

from Tuffix.Commands import KeywordContainer
from Tuffix.Configuration import BuildConfig, DEFAULT_BUILD_CONFIG
from Tuffix.Exceptions import *
from Tuffix.Status import *

parser = argparse.ArgumentParser()


parser.add_argument("--add", help="add a selected course", type=str)
parser.add_argument(
    "--custom", help="install a custom course requirement", type=str)

parser.add_argument("--remove", help="remove a selected course", type=str)

parser.add_argument(
    "--list-available", help="list currently available packages", action="store_true")

parser.add_argument(
    "--list-installed", help="list currently installed packages", action="store_true")
parser.add_argument(
    "--describe", help="give information about a selected package", type=str)
parser.add_argument("--init", help="initialize Tuffix", action="store_true")

arguments = parser.parse_args()


def valid_arguments(parser: argparse.ArgumentParser) -> list[tuple]:
    container = []
    for cmd in vars(parser).items():
        """
        TODO: Python 3.10 Feature
        match cmd:
            _, True:
                container.append(cmd)
        """
        name, status = cmd
        if(status):
            container.append(cmd)
    return container


def main(parser: argparse.ArgumentParser,
         arguments: list[str], build_config=DEFAULT_BUILD_CONFIG) -> None:

    if(not isinstance(build_config, BuildConfig) and
            isinstance(arguments, list)):
        raise ValueError

    parsed = parser.parse_args(arguments)
    current_arg = valid_arguments(parsed)[:1]  # taking the top most element
    name, _ = current_arg
    command_object = None

    for cmd in all_commands(build_config):
        if(cmd.name == name):
            command_object = cmd
            break

    if(not command_object):
        raise UsageError(f'[ERROR] Command {name} is not supported')


class argParseTests(unittest.TestCase):
    """
    Goal: test parser for Tuffix
    SRC: https://stackoverflow.com/a/18161115
    """

    def setUp(self):
        self.parser = parser
        self.keyword_container = KeywordContainer()

    def test_add(self):
        parsed = self.parser.parse_args(["--add", "121"])
        self.assertEqual("121", parsed.add)
        self.assertNotEqual("12", parsed.add)
        self.assertTrue("121" in self.keyword_container)
        # TODO: check if 121 is valid

    def test_remove(self):
        parsed = self.parser.parse_args(["--remove", "121"])
        self.assertEqual("121", parsed.remove)
        self.assertNotEqual("12", parsed.remove)
        self.assertTrue("121" in self.keyword_container)
        # TODO: check if 121 is valid

    def test_custom(self):
        parsed = self.parser.parse_args(["--custom", "/tmp/example.json"])
        # check if file exists
        # check if JSON is properly parsed
        self.assertTrue(os.path.exists(parsed.custom))


if __name__ == '__main__':
    unittest.main()
