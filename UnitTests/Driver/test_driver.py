from Tuffix.Driver import *
from Tuffix.Quieter import quiet
from Tuffix.Keywords import KeywordContainer
import unittest


class DriverTest(unittest.TestCase):
    def test_init(self):
        """
        Initialize Tuffix
        """

        command = "tuffix init"
        main(command.split())

    def test_list(self):
        """
        List all viable commands
        """

        command = "tuffix list"
        main(command.split())

    def test_describe(self):
        """
        Print all descriptions of keywords
        """

        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        k_container.container.sort(key=lambda x: x.name)
        for keyword in k_container.container:
            command = f"tuffix describe {keyword.name}"
            main(command.split())

    def test_add(self):
        """
        Add keyword `test`
        """

        command = "tuffix add tmux"
        main(command.split())

    def test_remove(self):
        """
        Remove keyword `test`
        """

        command = "tuffix remove tmux"
        main(command.split())

    def test_installed(self):
        """
        List all installed keywords
        """

        command = "tuffix installed"
        main(command.split())

    def test_status(self):
        """
        Print status command to the console
        """

        command = "tuffix status"
        main(command.split())

    def test_custom(self):
        """
        Install custom keyword via JSON
        """

        command = "tuffix custom json_payload/OSC.json"
        main(command.split())
