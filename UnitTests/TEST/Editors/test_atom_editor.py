#!/usr/bin/env python3.9


from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER
from Tuffix.Commands import InitCommand
from Tuffix.Editors import AtomKeyword
from Tuffix.Exceptions import UsageError
from Tuffix.Quieter import CapturingStderr, Capturing

import unittest
import pathlib
import re
import textwrap
import shutil
import subprocess

IGNORE_ME = True


class AtomKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()

        cls.Atom = AtomKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_available_links(self):
        """
        Check if the links associated with
        the keyword are up
        """

        try:
            DEFAULT_LINK_CHECKER.check_links(self.Atom.link_dictionary)
        except UsageError:
            self.assertTrue(False)

    def test_check_apm_candidates(self):
        """
        Check if APM can install any of the following plugins
        """

        uninstallable_packages = ["taco bell", "baco tell", "chipotle"]
        installable_packages = ["dbg-gdb", "dbg", "output-panel"]

        with CapturingStderr() as _:
            self.assertFalse(all([self.Atom.check_apm_candiate(_)
                                  for _ in uninstallable_packages]))
            self.assertTrue(all([self.Atom.check_apm_candiate(_)
                                 for _ in installable_packages]))

    def test_ppa_installation(self):
        """
        Ensure the PPA and GPG key have been
        properly installed
        """

        self.Atom.install_ppa()

        expression = """
        (?P<id>(([A-Z0-9]{4}\\s*)){10})
        uid\\s*[[].*[]]\\s*(?P<link>https\\:\\/\\/.*)\\s\\(.*\\)\\s[<](?P<email>.*)[>]
        """

        apt_key_re = re.compile(textwrap.dedent(expression).strip())
        apt_key = shutil.which("apt-key")
        bash = shutil.which("bash")

        apt_key_output = '\n'.join(subprocess.check_output(
            f'{apt_key} list',
            shell=True,
            executable=bash,
            encoding="utf-8",
            universal_newlines="\n").splitlines())

        if not(match := (apt_key_re.search(apt_key_output))):
            self.assertTrue(False)

        _id, _, _, link, email = match.groups()
        self._id = _id

        self.assertTrue(
            (link == "https://packagecloud.io/AtomEditor/atom") and
            (email == "support@packagecloud.io")
        )
        for _, artifcat in self.Atom.file_footprint.items():
            self.assertTrue(artifcat.is_file())

    def test_add(self):
        self.Atom.add(write=False)
        try:
            self.assertTrue(self.Atom.is_deb_package_installed('atom'))
        except EnvironmentError:
            self.assertTrue(False)

    def test_remove(self):
        self.Atom.remove(write=False)
        for _, artifcat in self.Atom.file_footprint.items():
            self.assertFalse(artifcat.is_file())
        try:
            self.assertFalse(self.Atom.is_deb_package_installed('atom'))
        except EnvironmentError:
            self.assertTrue(False)
