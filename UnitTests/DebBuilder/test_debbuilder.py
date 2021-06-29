#!/usr/bin/env python3.9

from Tuffix.DebBuilder import DebBuilder
from Tuffix.Exceptions import ParsingError
from Tuffix.Quieter import quiet

import unittest
import pathlib
import textwrap
import requests
import tarfile
import magic

class DebBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control_path = pathlib.Path("/tmp/control")
        cls.payload_path = pathlib.Path("/tmp/payload.tar.gz")
        cls.permissions = 0o775

        cls.children: list[pathlib.Path] = [
            pathlib.Path("DEBIAN"),
            pathlib.Path("usr")
        ]

        cls.Debbuilder = DebBuilder(
            name='unittestexample_jtool',
            payload=cls.payload_path    
        )

        cls.parent = pathlib.Path(f'/tmp/{cls.Debbuilder.name}')

        cls.scripts = [
            pathlib.Path("preinst"),
            pathlib.Path("postinst"),
            pathlib.Path("prerm"),
            pathlib.Path("postrm")
        ]
        for script in cls.scripts:
            script.touch()
            script.chmod(cls.permissions)

    def test_parse_control_file(self):
        """
        Test if the control file is properly formatted
        """

        with open(self.control_path, "w") as fp:
            contents = """
            Package: jtool
            Version: 1.0
            Section: debug
            Priority: optional
            Architecture: amd64
            Maintainer: JonathanLevin
            Description: tool for analyzing Mach-O files
            Depends: clang
            """
            contents = textwrap.dedent(contents).strip()
            contents += '\n'
            fp.write(contents)
        try:
            self.Debbuilder.parse_control_file(self.control_path)
        except ParsingError:
            self.assertTrue(False)
    
    def test_make_structure(self):
        """
        Ensure the structure is made during this function call
        """

        self.Debbuilder.make_structure(self.children)

        self.assertTrue(
            self.parent.is_dir() and
            all([(self.parent / path).is_dir() for path in self.children]))

    def test_make(self):
        # obtain the payload
        url = "http://newosxbook.com/tools/jtool2.tgz"

        content = requests.get(url).content

        with open(self.payload_path, "wb") as fp:
            fp.write(content)

        with tarfile.open(self.payload_path) as fp:
            fp.extractall(self.parent / self.children[1])

        perm = lambda x: oct(self.permissions) == oct(x.stat().st_mode & 0o777)

        self.assertTrue(
            all([perm(x) for x in self.scripts])
        )

        with quiet():
            self.Debbuilder.make(
                control=self.control_path,
                scripts=self.scripts,
                base_dir = [pathlib.Path('usr')],
                children = self.children
            ) 
        __m = magic.Magic(mime = True)

        self.assertTrue(
            self.Debbuilder.debian_path.exists() and
            __m.from_file(f'{self.Debbuilder.debian_path}') == "application/vnd.debian.binary-package"
        )
