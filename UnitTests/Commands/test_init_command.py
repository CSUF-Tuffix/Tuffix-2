#!/usr/bin/env python3.9

from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEBUG_BUILD_CONFIG
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

    def test_execute_no_args(self):
        """
        Make sure we throw a ValueError for not providing
        arguments to the function
        """
        __init = InitCommand(DEBUG_BUILD_CONFIG)
        try:
            __init.execute([])
        except ValueError:
            pass
        else:
            self.assertTrue(False)

    def test_create_state_directory(self):
        """
        Test if the state directory can be created
        """

        state_path, json_path = self.init.build_config.state_path, self.init.build_config.json_path

        init.create_state_directory()

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

        with open(git_configuration_file, "w") as fp:
            content = ''.join(fp.readlines())

        _user_re = re.compile("user = (?P<username>.*)")
        _email_re = re.compile("email = (?P<email>.*)")

        if not((user_match := _user_re.search(content)) and
               (email_match := _email_re.search(content))):
            self.assertTrue(False)

        user, mail = user_match.group("username"), email_match.group("email")

        self.assertTrue(
            (user == username) and
            (email == mail)
        )

    def test_configure_ppa(self):
        tuffix_list = pathlib.Path("/etc/apt/sources.list.d/tuffix.list")
        self.init.configure_ppa()

        if not(tuffix_list.is_file() or
               (apt_key := shutil.which("apt-key")) or
               (bash := shutil.which("bash"))):
            self.assertTrue(False)

        # NOTE: this might need to change when I leave the project

        expression = """
        (?P<id>(([A-Za-z0-9]{4}\s*)){10})
        uid\s*\[.*\]\s*(?P<author>([A-Za-z]+\s?)+)\<(?P<email>.*)\>
        """

        apt_key_re = re.compile(textwrap.dedent(expression).strip())
        apt_key_output = '\n'.join(subprocess.check_output(
            f'{apt_key} list',
            shell=True,
            executable=bash,
            encoding="utf-8",
            universal_newlines="\n").splitlines())

        if not(match := (apt_key_re.search(apt_key_output))):
            self.assertTrue(False)

        _id, author, email = match.groups()

        self.assertTrue(
            (author == "Jared Dyreson") and
            (email == "jareddyreson@csu.fullerton.edu")
        )

        removal_output = '\n'.join(subprocess.check_output(
            f'{apt_key} del {_id}',
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

        self.init.install_atom()
        current_state = read_state(self.init.build_config)
        self.assertTrue("atom" in current_state.editors)

        AtomKeyword().remove()
        new_state = read_state(self.init.build_config)

        self.assertTrue("atom" not in current_state.editors)
