from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.Keywords import partial_class, CustomPayload
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

import json
import unittest
import pathlib

"""
return partial_class(
    (custom.name,
     f'created by {custom.instructor} for {custom.name}',
     custom.packages),
    AbstractKeyword,
    build_config)
"""


class PartialClassTest(unittest.TestCase):
    def from_dict_template(self, container: dict):
        __custom = CustomPayload(container)
        __custom_class = partial_class(
            (
                __custom.name,
                f"created by {__custom.instructor} for {__custom.name}",
                __custom.packages,
            ),
            AbstractKeyword,
            DEBUG_BUILD_CONFIG,
        )

        self.assertTrue(issubclass(__custom_class, AbstractKeyword))

    def test_from_dictionary(self):
        container = {
            "name": "Operating System Concepts",
            "instructor": "William McCarthy",
            "packages": ["vim"],
        }

        self.from_dict_template(container)

    def test_from_json_container(self):
        container = {
            "name": "Operating System Concepts",
            "instructor": "William McCarthy",
            "packages": ["vim", "emacs", "cowsay"],
        }

        json_path = pathlib.Path("/tmp/test_from_json_container.json")
        with open(json_path, "w") as fp:
            json.dump(container, fp)

        # pretend something has happened
        # this is a slightly useless test

        with open(json_path, encoding="utf-8") as fp:
            content = json.loads(fp.read())

        self.from_dict_template(content)
