#!/usr/bin/env python3.9

from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
import unittest


class AbstractKeywordTest(unittest.TestCase):
    def test_init_default(self):
        """
        Test if the default build configuration
        will work
        """

        try:
            _ = AbstractKeyword(
                DEFAULT_BUILD_CONFIG, "test", "this is an example AbstractKeyword", []
            )
        except ValueError:
            self.assertTrue(False)

    def test_init_failure(self):
        """
        Test if the default build configuration
        will work with a long long name
        It should fail yet succeed in testing
        """

        try:
            _ = AbstractKeyword(
                DEFAULT_BUILD_CONFIG,
                "this is a long long name that should surely break",
                "long long description",
                [],
            )
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_add(self):
        """
        Test the add function for the base class
        This should raise a `NotImplementedError` by default
        """

        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            ["cowsay"],
        )
        try:
            AbstractKeywordTest.add()
        except NotImplementedError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_remove(self):
        """
        Test the remove function for the base class
        This should raise a `NotImplementedError` by default
        """

        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            ["cowsay"],
        )
        try:
            AbstractKeywordTest.remove()
        except NotImplementedError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_check_install_candidates_vetted(self):
        """
        This checks the installability of a package
        These should work because they were dependencies of the `tuffix` Debian installer
        """

        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            [
                "git",
                "openssh-client",
                "openssh-server",
                "python3",
                "python3-pip",
                "vim",
            ],
        )
        try:
            AbstractKeywordTest.check_candiates()
        except KeyError:
            self.assertTrue(False)

    def test_check_install_candidates_not_present(self):
        """
        This checks the installability of a package
        These should fail because they do not exist
        """

        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            ["kevinwortman", "jareddyreson", "paulinventado", "mshafae"],
        )
        try:
            AbstractKeywordTest.check_candiates()
        except KeyError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_check_is_installed_vetted(self):
        """
        This checks to see if the contents of the AbstractKeyword
        have actually been installed
        These should work because they were installed during the `tuffix.deb` installation
        """

        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            [
                "git",
                "openssh-client",
                "openssh-server",
                "python3",
                "python3-pip",
                "vim",
            ],
        )
        for package in AbstractKeywordTest.packages:
            try:
                status = AbstractKeywordTest.is_deb_package_installed(package)
                self.assertTrue(status)
            except KeyError:
                # package is somehow not found?
                self.assertTrue(False)

    def test_check_is_installed_not_present(self):
        """
        This checks to see if the contents of the AbstractKeyword
        have actually been installed
        These should work because the latest kernel version is 5.8 and I assume that the user does not have these installed by default
        """
        AbstractKeywordTest = AbstractKeyword(
            DEFAULT_BUILD_CONFIG,
            "test",
            "this is an example AbstractKeyword",
            ["unicorn"],
        )
        for package in AbstractKeywordTest.packages:
            try:
                status = AbstractKeywordTest.is_deb_package_installed(package)
                self.assertFalse(status)
            except KeyError:
                # package is somehow not found?
                self.assertTrue(False)
