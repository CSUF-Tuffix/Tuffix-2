#!/usr/bin/env python3.9

from Tuffix.Commands import CustomCommand

from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest
import textwrap
import pathlib
import json

class CustomCommandTest(unittest.TestCase):
    def test_init(self):
        """
        Test the __init__ function
        """
        try:
            CustomCommand(DEFAULT_BUILD_CONFIG)
        except ValueError:
            self.assertTrue(False)

    def test_execute_valid_path(self):
        """
        Test execute with valid payload
        """

        payload = {
            "name": "python",
            "instructor": "Jared Dyreson",
            "packages": ["python3", "python3-pip", "python3-virtualenv"]
        }

        payload_path = pathlib.Path("/tmp/python_course.json")

        with open(payload_path, "w") as fp:
            json.dump(payload, fp)
