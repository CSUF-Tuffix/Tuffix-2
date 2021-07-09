#!/usr/bin/env python3.9

from Tuffix.Exceptions import LinkError
from Tuffix.LinkChecker import LinkPacket, LinkChecker

from Tuffix.Editors import AtomKeyword
from Tuffix.Keywords import BaseKeyword
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG

import unittest


class LinkCheckerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Linker = LinkChecker()

    def test_alive_links(self):
        """
        Test for links that are active
        """

        active_links: list[LinkPacket] = [
            LinkPacket(
                link="https://google.com",
                is_git=False),
            LinkPacket(
                link="https://github.com",
                is_git=False),
            LinkPacket(
                link="http://www.fullerton.edu/",
                is_git=False),
            LinkPacket(
                link="https://github.com/JaredDyreson/thin-mint.git",
                is_git=True),
            LinkPacket(
                link="https://github.com/JaredDyreson/Tuffix-Lib.git",
                is_git=True),
            LinkPacket(
                link="https://github.com/JaredDyreson/StarSort.git",
                is_git=True)]

        for link in active_links:
            try:
                status, code = self.Linker.link_up(link)
                self.assertTrue(
                    isinstance(status, bool) and
                    (status) and
                    isinstance(code, int)
                )
            except ValueError:
                self.assertTrue(False)

    def test_dead_links(self):
        """
        Test for links that are dead
        """

        active_links: list[LinkPacket] = [
            LinkPacket(
                link="https://thisshouldnotbeavalidurlbecauseisaidso.com",
                is_git=False),
            LinkPacket(
                link="https://tacobellisthebestever.com",
                is_git=False),
            LinkPacket(
                link="https://thislinkshouldbedead.xyz",
                is_git=False),
            LinkPacket(
                link="https://github.com/JaredDyreson/tacobell.git",
                is_git=True),
            LinkPacket(
                link="https://github.com/JaredDyreson/bacotellmenu.git",
                is_git=True),
            LinkPacket(
                link="https://github.com/JaredDyreson/JoJoRabbit.git",
                is_git=True)]

        for link in active_links:
            try:
                status, code = self.Linker.link_up(link)
                self.assertTrue(
                    isinstance(status, bool) and
                    (status == False) and
                    isinstance(code, int)
                )
            except ValueError:
                self.assertTrue(False)

    def test_class_attribute(self):
        """
        Test classes that contain a dictionary holding the links
        for each of the dependencies
        """

        Atom = AtomKeyword(DEFAULT_BUILD_CONFIG)
        Base = BaseKeyword(DEFAULT_BUILD_CONFIG)

        self.assertTrue(hasattr(Atom, 'link_dictionary'))
        self.assertTrue(hasattr(Base, 'link_dictionary'))

        try:
            self.Linker.check_links(Atom.link_dictionary)
        except LinkError:
            self.assertTrue(False)

        try:
            self.Linker.check_links(Base.link_dictionary)
        except LinkError:
            self.assertTrue(False)
