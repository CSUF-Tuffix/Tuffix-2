#!/usr/bin/env python3.9

from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state
from Tuffix.Editors import AtomKeyword
from Tuffix.Quieter import Capturing
from Tuffix.SudoRun import SudoRun

import pathlib
import re
import shutil
import subprocess
import termcolor
import textwrap
import unittest


class InitCommandTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.init = InitCommand(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        parent = cls.init.build_config.state_path.parent
        shutil.rmtree(parent)

    def test_create_state_directory(self):
        """
        Test if the state directory can be created
        """

        state_path, json_path = self.init.build_config.state_path, self.init.build_config.json_state_path

        self.init.create_state_directory()

        # check if Tuffix was successfully been configured
        if not(state_path.is_file() and json_path.is_dir()):
            self.assertTrue(False)

    def test_git_configuration(self):
        """
        Test if the git configuration works
        by checking the content of /home/{user}/.gitconfig
        """

        username, email = "tuffytitan", "tuffy@csu.fullerton.edu"
        git_configuration_file = pathlib.Path(
            f'/home/{SudoRun().whoami}/.gitconfig')

        with Capturing() as output:
            self.init.configure_git(username=username, mail=email)

        self.assertTrue(
            termcolor.colored("Successfully configured git", 'green') ==
            output[0])

        with open(git_configuration_file, "r") as fp:
            content = ''.join(fp.readlines())

        _user_re = re.compile("name = (?P<username>.*)")
        _email_re = re.compile("email = (?P<email>.*)")

        user_match = _user_re.search(content)
        email_match = _email_re.search(content)

        if not(user_match and email_match):
            print(user_match)
            print(email_match)
            self.assertTrue(False)

        # if not((user_match := _user_re.search(content)) and
            # (email_match := _email_re.search(content))):
            # print(user_match)
            # print(email_match)
            # self.assertTrue(False)

        user, mail = user_match.group("username"), email_match.group("email")

        self.assertTrue(
            (user == username) and
            (email == mail)
        )

    def test_configure_ppa(self):
        tuffix_list = pathlib.Path("/etc/apt/sources.list.d/tuffix.list")
        self.init.configure_ppa()

        if not(tuffix_list.is_file()):
            self.assertTrue(False)

        expression = """
        (?P<id>(([A-Za-z0-9]{4}\\s*)){10})
        uid\\s*\\[.*\\]\\s*(?P<author>([A-Za-z]+\\s?)+)\\<(?P<email>.*)\\>
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

        _id, _, _, author, _, email = match.groups()

        self.assertTrue(
            (author == "Jared Dyreson ") and
            (email == "jareddyreson@csu.fullerton.edu")
        )

        removal_output = '\n'.join(subprocess.check_output(
            f'{apt_key} del "{_id}"',
            shell=True,
            executable=bash,
            encoding="utf-8",
            universal_newlines="\n").splitlines())

        self.assertTrue(removal_output == "OK")

        tuffix_list.unlink()
        self.assertFalse(tuffix_list.is_file())

    def test_install_atom(self):
        """
        This is a higher level testing of AtomKeyword
        Please consult UnitTests/Editors/test_atom_keyword.py for a micro perspective
        """

        self.init.install_atom(write=True)
        current_state = read_state(self.init.build_config)
        self.assertTrue("atom" in current_state.editors)

        AtomKeyword(self.init.build_config).remove(write=True)
        new_state = read_state(self.init.build_config)

        self.assertTrue(new_state.editors == [])
