#!/usr/bin/env python3.9


from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import EditorBaseKeyword

import unittest


class EditorBaseKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG, DEBUG_BUILD_CONFIG.version, [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_editor_base_constructor(self):
        """
        Test base constructor
        """

        try:
            ExampleEditor = EditorBaseKeyword(
                DEBUG_BUILD_CONFIG, "example", "this is an example of the base class"
            )
        except ValueError:
            self.assertTrue(False)

    def test_update_state(self):
        """
        Ensure we can write to the state configuration file
        """

        ExampleEditor = EditorBaseKeyword(
            DEBUG_BUILD_CONFIG, "example", "this is an example of the base class"
        )

        current_state = read_state(DEBUG_BUILD_CONFIG)

        self.assertTrue(current_state.editors == [])

        # "install" the current keyword

        ExampleEditor.rewrite_state(arguments=[ExampleEditor.name], install=True)

        installed_example_state = read_state(DEBUG_BUILD_CONFIG)

        self.assertTrue(installed_example_state.editors == [ExampleEditor.name])

        # "remove" the current keword

        ExampleEditor.rewrite_state(arguments=[ExampleEditor.name], install=False)

        removed_example_state = read_state(DEBUG_BUILD_CONFIG)

        self.assertTrue(removed_example_state.editors == [])
