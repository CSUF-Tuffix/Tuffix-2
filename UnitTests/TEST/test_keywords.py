import unittest

from Tuffix.Keywords import *
from Tuffix.Editors import EditorKeywordContainer
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER
from Tuffix.Constants import *


class KeywordTest(unittest.TestCase):
    def test_editors(self):
        k_container = EditorKeywordContainer(DEFAULT_BUILD_CONFIG)

        for keyword in k_container.container:
            print(f'checking editor {keyword.name}')
            try:
                keyword.check_candiates()
                if(hasattr(keyword, 'link_dictionary')):
                    DEFAULT_LINK_CHECKER.check_links(keyword.link_dictionary)
            except KeyError:
                print(f'[INTERNAL ERROR] {keyword.name} has failed')
                self.assertTrue(False)
            print(f'[INTERNAL SUCCESS] {keyword.name} has passed')
