#!/usr/bin/env python3.9

from UnitTests.BaseEditorTest import TestEditorGeneric

from Tuffix.Configuration import DEBUG_BUILD_CONFIG
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER
from Tuffix.Commands import InitCommand
from Tuffix.Editors import AtomKeyword
from Tuffix.Quieter import CapturingStderr

from UnitTests.BaseEditorTest import TestEditorGeneric

import re
import textwrap
import shutil
import subprocess

import unittest

class AtomKeywordTest(TestEditorGeneric):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(AtomKeyword(DEBUG_BUILD_CONFIG))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.keyword.write_to_sources(cls.keyword.repo_payload, False)

    def ppa_installation_generic(self):
        """
        Ensure the PPA and GPG key have been
        properly installed
        """

        self.keyword.install_ppa()

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

    def test_add(self):
        self.generic_check_add()
        self.ppa_installation_generic()

    def test_remove(self):
        self.generic_check_remove()

    @unittest.skip("started breaking?")
    def test_check_apm_candidates(self):
        """
        Check if APM can install any of the following plugins
        """

        uninstallable_packages = ["taco bell", "baco tell", "chipotle"]
        installable_packages = ["dbg-gdb", "dbg", "output-panel"]

        with CapturingStderr() as _:
            self.assertFalse(all([self.keyword.check_apm_candiate(_)
                                  for _ in uninstallable_packages]))
            self.assertTrue(all([self.keyword.check_apm_candiate(_)
                                 for _ in installable_packages]))
