#!/usr/bin/env python3.9

from Tuffix.UtilityFunctions import *
from Tuffix.Exceptions import *
from Tuffix.SudoRun import *
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from UnitTests import SequentialTest

import os
import shutil
import pathlib
import unittest
import getpass


class UtilityFunctionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_configuration = DEFAULT_BUILD_CONFIG
        # cls.background_path = "/tmp/background.png"

    # def test_create_state_directory(self):
        # """
        # Check if we can create the state directory
        # """
        # #  if `tuffix init` has already occurred

        # if not(os.path.exists(self.build_configuration.state_path)):
        # self.assertTrue(True)
        # return

        # try:
        # create_state_directory(
        # self.build_configuration)
        # except UsageError:
        # self.assertTrue(False)
        # if not(os.path.exists(self.build_configuration.state_path)):
        # self.assertTrue(False)
        # # shutil.rmtree(self.build_configuration.state_path.parent.absolute())

    # def test_distrib_codename(self):
        # # NOTE : this also tests parse_distrib_codename
        # # Also note that this method should be depreciated in favor of LSBParser

        # try:
        # result = distrib_codename()
        # self.assertTrue(isinstance(result, str))
        # except (OSError, FileNotFoundError):
        # self.assertTrue(False)

    # def test_is_package_installed(self):
        # example_package = "python3"
        # try:
        # is_deb_package_installed(example_package)
        # except EnvironmentError:
        # self.assertTrue(False)

    # def test_ensure_root_access(self):
        # # this function needs to be run as non-root users
        # user = getpass.getuser()
        # try:
        # ensure_root_access()
        # except UsageError:
        # self.assertTrue((user != "root"))
        # else:
        # # we are root
        # self.assertTrue(True)

    # def test_ensure_ubuntu(self):
        # # Please try this on Ubuntu
        # try:
        # ensure_ubuntu()
        # except UsageError:
        # self.assertTrue(False)

    # def test_shell_command_presence(self):
        # try:
        # ensure_shell_command_exists("spongebob")
        # except EnvironmentError:
        # pass
        # else:
        # self.assertTrue(False)

        # try:
        # ensure_shell_command_exists("echo")
        # except EnvironmentError:
        # # echo should be installed by default
        # self.assertTrue(False)

    def test_get_user_submitted_wallpaper(self):
        _response = retreieve_user_submitted_wallpaper()
        if not(isinstance(_response, tuple)):
            self.assertTrue(False)
        try:
            file_ = get_user_submitted_wallpaper(_response)
        except EnvironmentError:
            self.assertFalse(True)

        if not(isinstance(file_, pathlib.Path)):
            self.assertTrue(False)
        # set_background(destination)
        # sudo.run(f"gsettings set org.gnome.desktop.background picture-uri file://{destination}", "jared")

    # def test_set_background(self):
        # try:
        # except EnvironmentError:
            # self.assertTrue(False)
