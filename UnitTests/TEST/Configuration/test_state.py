#!/usr/bin/env python3.9

from Tuffix.Configuration import State, read_state, BuildConfig, DEBUG_BUILD_CONFIG, DEFAULT_BUILD_CONFIG
from Tuffix.Commands import InitCommand
from Tuffix.Exceptions import EnvironmentError as EnvError

# NOTE : naming conflict from std::EnvironmentError
# SEVERITY: moderate

import unittest
import json
import pathlib


class StateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.another = State(DEBUG_BUILD_CONFIG,
                            DEBUG_BUILD_CONFIG.version,
                            ["__packages__"], ["__editor__"])

        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()

        cls.state.write()

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_eq_operator(self):
        self.assertFalse(
            self.state == self.another)

    def test_write(self):
        self.assertTrue(
            self.state.build_config.state_path.is_file())

    def test_read_state(self):
        # init has not been completed yet
        # OSError, FileNotFoundError


        self.Init.remove_state_directory()

        try:
            read_state(DEBUG_BUILD_CONFIG)
        except (FileNotFoundError, EnvError):
            self.Init.create_state_directory()
            self.state.write()
        else:
            self.assertTrue(False)

        original_state = read_state(DEBUG_BUILD_CONFIG)

        corrupted_payload = {"malformed": "payload"}
        with open(DEBUG_BUILD_CONFIG.state_path, "w") as fp:
            json.dump(corrupted_payload, fp)

        invalid_version = {
            "version": "baconandeggs",
            "installed": [],
            "editors": []
        }

        with open(DEBUG_BUILD_CONFIG.state_path, "w") as fp:
            json.dump(invalid_version, fp)

        # malformed version
        # packaging.version.InvalidVersion

        try:
            read_state(DEBUG_BUILD_CONFIG)
        except EnvError:
            self.state = self.another
        else:
            self.assertTrue(False)

        # missing data
        # KeyError

        try:
            read_state(DEBUG_BUILD_CONFIG)
        except EnvError:
            self.state = self.another
        else:
            self.assertTrue(False)

        invalid_data_components = {
            "version": "1.0",
            "installed": set(),
            "editors": []
        }
        # Data is incorrect
        # ValueError <- given in constructor of State()
        try:
            read_state(DEBUG_BUILD_CONFIG)
        except EnvError:
            self.state = self.another
        else:
            self.assertTrue(False)

        # NOTE : unsure how to make JSON data malformed
