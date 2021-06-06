#!/usr/bin/env python3.9

"""
TODO: have the unit tests run in order
"""


from Tuffix.Driver import *
import unittest

class DriverTest(unittest.TestCase):
    def test_init(self):
        """
        Initialize Tuffix
        """

        command = "tuffix init"
        main(command.split())

    def test_editor(self):
        """
        Add and remove an editor: emacs
        """

        command = "tuffix editor add emacs"
        main(command.split())
        command = "tuffix editor remove emacs"
        main(command.split())

    # def test_list(self):
        # """
        # List all viable commands
        # """

        # command = "tuffix list"
        # main(command.split())

    # def test_describe(self):
        # """
        # Print all descriptions of keywords
        # """

        # k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        # k_container.container.sort(key=lambda x: x.name)
        # for keyword in k_container.container:
            # command = f'tuffix describe {keyword.name}'
            # main(command.split())

    # def test_add(self):
        # """
        # Add keyword `test`
        # """

        # command = "tuffix add test"
        # main(command.split())

    # def test_remove(self):
        # """
        # Remove keyword `test`
        # """

        # command = "tuffix remove test"
        # main(command.split())

    # def test_installed(self):
        # """
        # List all installed keywords
        # """

        # command = "tuffix installed"
        # main(command.split())

    # def test_status(self):
        # """
        # Print status command to the console
        # """

        # command = "tuffix status"
        # main(command.split())

    # def test_custom(self):
        # """
        # Install custom keyword via JSON
        # """

        # command = "tuffix custom json_payload/OSC.json"
        # main(command.split())


    # def test_sysupgrade(self):
        # """
        # Equivalent of running `sudo apt-get upgrade -y`
        # """

        # command = "tuffix supgrade"
        # main(command.split())

    # def __dir__(self):
        # return [
            # # "test_init",
            # # "test_editor",
            # "test_list",
            # "test_describe",
            # # "test_add",
            # # "test_remove",
            # # "test_installed",
            # # "test_status",
            # # "test_custom",
            # # "test_sysupgrade"
        # ]
