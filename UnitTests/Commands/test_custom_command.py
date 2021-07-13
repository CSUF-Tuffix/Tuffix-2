#!/usr/bin/env python3.9

from Tuffix.Commands import CustomCommand, InitCommand, RemoveCommand, AddRemoveHelper

from Tuffix.Configuration import DEBUG_BUILD_CONFIG, State
from Tuffix.CustomPayload import CustomPayload

import unittest
import textwrap
import pathlib
import json
import shutil
import os


class CustomCommandTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.custom = CustomCommand(DEBUG_BUILD_CONFIG)
        cls.init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.init.create_state_directory()
        cls.state.write()

    @classmethod
    def tearDownClass(cls):
        pass
        # parent = cls.custom.build_config.state_path.parent
        # shutil.rmtree(parent)

    @unittest.skip("")
    def test_init(self):
        """
        Test the __init__ function
        """
        try:
            CustomCommand(DEBUG_BUILD_CONFIG)
        except ValueError:
            self.assertTrue(False)

    def test_execute_valid_path(self):
        """
        Test execute with valid payload
        """

        payload = {
            "name": "ruby",
            "instructor": "Jared Dyreson",
            "packages": ["ruby-full"]
        }

        payload_path = pathlib.Path("/tmp/ruby.json")

        with open(payload_path, "w") as fp:
            json.dump(payload, fp)

        custom = CustomCommand(DEBUG_BUILD_CONFIG)
        custom.execute(arguments=[str(payload_path.resolve())])

        print(os.listdir("/tmp/tuffix/json_payloads"))

        payload_path.unlink()

    @unittest.skip("")
    def test_execute_invalid_path(self):
        """
        Test execute with invalid payload
        """

        custom = CustomCommand(DEBUG_BUILD_CONFIG)
        try:
            custom.execute(arguments=['/tmp/this_is_a_fake_path.json'])
        except FileNotFoundError:
            pass
        else:
            self.assertTrue(False)

    @unittest.skip("")
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
        custom = CustomCommand(DEBUG_BUILD_CONFIG)
        path = "/tmp/malformed_payload.json"

        for payload in payloads:
            with open(path, "w") as fp:
                json.dump(payload, fp)
            try:
                custom.execute(arguments=[path])
            except (KeyError, ValueError):
                pass
            else:
                self.assertTrue(False)

    def test_remove_custom(self):
        helper_remove = AddRemoveHelper(DEBUG_BUILD_CONFIG, 'remove')
        __search = helper_remove.search("ruby")
        print(__search)
        # Test Remove
        helper_remove.run_commands(
            container=[__search], install=False)
        updated_state = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("ruby" not in updated_state.installed)
