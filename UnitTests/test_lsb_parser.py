#!/usr/bin/env python3.9

"""
pure Python equivalent of lsb_release, because I wanted to OKAY?
inspiration from this: https://chromium.googlesource.com/chromiumos/docs/+/HEAD/lsb-release.md
AUTHOR: Jared Dyreson
"""

from Tuffix.LSBParser import lsb_parser
import unittest


class LSBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # NOTE: test constructor
        try:
            cls._lsb_parser = lsb_parser()
        except EnvironmentError as error:
            raise AssertionError(f'{error}')

    def test_load(self):
        self.assertTrue(
            isinstance(self._lsb_parser.file_map, dict)
        )

    def test_lsb_version(self):
        try:
            _version = self._lsb_parser.lsb_version()
        except ValueError as error:
            # parsing error
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        self.assertTrue(
            isinstance(_version, float)
        )

    def test_lsb_id(self):
        _id = self._lsb_parser.lsb_id()

        self.assertTrue(
            isinstance(_id, str)
        )

    def test_lsb_type(self):
        _type = self._lsb_parser.lsb_release_type()

        self.assertTrue(
            isinstance(_type, str)
        )

    def test_lsb_description(self):
        _description = self._lsb_parser.lsb_distrib_description()

        self.assertTrue(
            isinstance(_description, str)
        )


if __name__ == '__main__':
    unittest.main()
