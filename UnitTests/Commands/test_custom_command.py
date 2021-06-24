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

        custom = CustomCommand(DEFAULT_BUILD_CONFIG)
        custom.execute(arguments=[payload_path.resolve()])

        payload_path.unlink()

    def test_execute_invalid_path(self):
        """
        Test execute with invalid payload
        """

        custom = CustomCommand(DEFAULT_BUILD_CONFIG)
        try:
            custom.execute(arguments=['/tmp/this_is_a_fake_path.json'])
        except FileNotFoundError:
            pass
        else:
            self.assertTrue(False)

    def test_execute_malformed_data(self):
        payloads = [
            {  # missing name
                "instructor": "Jared Dyreson",
                "packages": ["python3", "python3-pip", "python3-virtualenv"]
            },
            {  # missing instructor
                "name": "python",
                "packages": ["python3", "python3-pip", "python3-virtualenv"]
            },
            {  # missing packages
                "name": "python",
                "instructor": "Jared Dyreson",
            }
        ]
        custom = CustomCommand(DEFAULT_BUILD_CONFIG)
        path = "/tmp/malformed_payload.json"

        for payload in payloads:
            with open(path, "w") as fp:
                json.dump(payload, fp)
            try:
                custom.execute(arguments=[path])
            except KeyError:
                pass
            else:
                self.assertTrue(False)
