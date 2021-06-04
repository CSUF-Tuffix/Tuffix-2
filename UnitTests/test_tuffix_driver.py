#!/usr/bin/env python3.9

from Tuffix.Driver import *
import unittest


class DriverTest(unittest.TestCase):

    def test_init(self):
        command = "tuffix init"
        main(command.split())

    def test_list(self):
        command = "tuffix list"
        main(command.split())

    def test_describe(self):
        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        k_container.container.sort(key=lambda x: x.name)
        for keyword in k_container.container:
            command = f'tuffix describe {keyword.name}'
            main(command.split())

    def test_add(self):
        command = "tuffix add test"
        main(command.split())

    def test_remove(self):
        command = "tuffix remove test"
        main(command.split())

    def test_installed(self):
        command = "tuffix installed"
        main(command.split())

    def test_status(self):
        command = "tuffix status"
        main(command.split())

    def test_custom(self):
        command = "tuffix custom json_payload/OSC.json"
        main(command.split())


    def test_sysupgrade(self):
        command = "tuffix supgrade"
        main(command.split())
