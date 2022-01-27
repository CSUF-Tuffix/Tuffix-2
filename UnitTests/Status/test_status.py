"""
Unit tests for Status API
AUTHOR: Jared Dyreson
"""

import unittest
from Tuffix.Status import *
from Tuffix.Exceptions import *
from subprocess import CalledProcessError
from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.Commands import InitCommand


class StatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.init.create_state_directory()

    @classmethod
    def tearDownClass(cls):
        cls.init.remove_state_directory()

    def test_is_ubuntu(self):
        """
        Is the platform Ubuntu?
        """
        try:
            ensure_ubuntu()
        except UsageError:
            self.assertTrue(False)

    def test_is_root(self):
        """
        Does user have root privileges
        """

        try:
            ensure_root_access()
        except UsageError:
            self.assertTrue(False)

    def test_in_VM(self):
        """
        Assuming we are running in a VM for testing
        """

        self.assertTrue(not (output := in_VM()) and isinstance(output, bool))

    def test_cpu_information(self):
        _re = re.compile(".*\\([\\d]+ core\\(s\\)\\)")
        self.assertTrue(
            (output := cpu_information())
            and isinstance(output, str)
            and ((match := _re.match(output)))
        )

    def test_host(self):
        _re = re.compile("([\\w|\\W]+)\\@([\\w|\\W]+)")

        self.assertTrue(
            (output := host())
            and isinstance(output, str)
            and (match := _re.match(output))
        )

    def test_current_operating_system(self):
        try:
            self.assertTrue(
                (output := current_operating_system()) and isinstance(output, str)
            )
        except (EnvironmentError, ParsingError):
            self.assertTrue(False)

    def test_current_kernel_revision(self):
        self.assertTrue(isinstance(current_kernel_revision(), str))

    def test_current_time(self):
        self.assertTrue(isinstance(current_time(), str))

    def test_current_model(self):

        try:
            self.assertTrue((match := current_model()) and isinstance(match, str))
        except EnvironmentError as error:
            self.assertTrue(False)

    def test_current_uptime(self):
        _re = re.compile(
            "[\\d]+ day\\(s\\)\\, [\\d]+ hour\\(s\\)\\, [\\d]+ minute\\(s\\), [\\d]+ second\\(s\\)"
        )
        try:
            self.assertTrue(
                (output := current_uptime())
                and isinstance(output, str)
                and (match := _re.match(output))
            )
        except (EnvironmentError, ValueError):
            # cannot find proper device files
            # parsing error in /proc/uptime
            self.assertTrue(False)

    def test_memory_information(self):
        try:
            self.assertTrue(
                (output := memory_information()) and isinstance(output, int)
            )
        except (EnvironmentError, ValueError):
            # cannot find meminfo
            # parsing error in /proc/meminfo
            self.assertTrue(False)

    def test_graphics_information(self):
        try:
            self.assertTrue(
                (graphics := graphics_information())
                and ((argc := len(graphics)) == 2)
                and isinstance(graphics, tuple)
                and all([isinstance(_, str) for _ in graphics])
            )
        except EnvironmentError:
            # could not find bash or lspci
            self.assertTrue(False)

    def test_git_configuration(self):
        try:
            self.assertTrue(
                (output := list_git_configuration())
                and ((argc := len(output)) == 2)
                and isinstance(output, list)
                and all([isinstance(_, str) for _ in output])
            )
        except EnvironmentError:
            self.assertTrue(False)

    def test_has_internet(self):
        try:
            self.assertTrue(
                (information := has_internet()) and isinstance(information, bool)
            )
        except (EnvironmentError, ValueError):
            # not linux
            # parsing error

            self.assertTrue(False)

    def test_currently_installed_targets(self):
        try:
            targets = currently_installed_targets(DEBUG_BUILD_CONFIG)
            self.assertTrue(
                isinstance(targets, list) and all([isinstance(_, str) for _ in targets])
            )
        except EnvironmentError:
            # error in read_state
            self.assertTrue(False)

    def test_status(self):
        try:
            self.assertTrue(
                (_status := status(DEBUG_BUILD_CONFIG))
                and isinstance(_status, tuple)
                and all([isinstance(_, str) for _ in _status])
            )
        except EnvironmentError:
            # general exception, too much can go wrong here
            self.assertTrue(False)

    def test_system_shell(self):
        try:
            self.assertTrue((shell := system_shell()) and isinstance(shell, str))
        except (EnvironmentError, ValueError):
            # not unix
            # cannot parse /etc/passwd or shell version
            self.assertTrue(False)

    def test_terminal_emulator(self):
        try:
            self.assertTrue(
                (emulator := system_terminal_emulator()) and isinstance(emulator, str)
            )
        except ValueError:
            # shell output parsing error
            self.assertTrue(False)
