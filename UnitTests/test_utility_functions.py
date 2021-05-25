#!/usr/bin/env python3.9

import Tuffix
import os
import shutil
import pathlib


class UtilityFunctionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_configuration = Tuffix.Configuration.DEFAULT_BUILD_CONFIG
        # cls.background_path = "/tmp/background.png"

    def test_distrib_codename(self):
        # NOTE : this also tests parse_distrib_codename
        try:
            result = Tuffix.UtilityFunctions.distrib_codename()
            self.assertTrue(isinstance(result, str))
        except (OSError, FileNotFoundError):
            self.assertTrue(False)

    def test_is_package_installed(self):
        example_package = "cowsay"
        try:
            Tuffix.UtilityFunctions.is_deb_package_installed(example_package)
        except EnvironmentError:
            self.assertTrue(False)

    def test_ensure_root_access(self):
        # this function needs to be run as non-root users
        try:
            Tuffix.UtilityFunctions.ensure_root_access()
        except Tuffix.Exceptions.UsageError:
            pass

    def test_ensure_ubuntu(self):
        # Please try this on Ubuntu
        try:
            Tuffix.UtilityFunctions.ensure_ubuntu()
        except Tuffix.Exceptions.UsageError:
            self.assertTrue(False)

    def test_shell_command_presence(self):
        try:
            Tuffix.UtilityFunctions.ensure_shell_command_exists("spongebob")
        except EnvironmentError:
            pass
        else:
            self.assertTrue(False)

        try:
            Tuffix.UtilityFunctions.ensure_shell_command_exists("echo")
        except EnvironmentError:
            # echo should be installed by default
            self.assertTrue(False)

    def test_create_state_directory(self):
        try:
            Tuffix.UtilityFunctions.create_state_directory(
                self.build_configuration)
        except Tuffix.Exceptions.UsageError:
            self.assertTrue(False)

        if not(os.path.isdir(self.build_configuration)):
            self.assertTrue(False)

        shutil.rmtree(self.build_configuration)

    # def test_set_background(self):
    def test_get_user_submitted_wallpaper(self):
        # NOTE: currently not taking input for this function
        # please update when it takes in a dictinoary.
        try:
            Tuffix.UtilityFunctions.get_user_submitted_wallpaper()
        except EnvironmentError:
            self.assertFalse(True)

        wallpaper_dir = f'{pathlib.Path.home()}/Pictures/Wallpapers'
        destination = f'{wallpaper_dir}/SpacialRend.jpg'

        if not(os.path.exists(destination)):
            self.assertTrue(False)
