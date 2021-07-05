import unittest

from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
from Tuffix.Keywords import KeywordContainer
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER


class KeywordTest(unittest.TestCase):
    def test_keywords_and_editors(self):
        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        for keyword in k_container.container:
            print(f'checking element {keyword.name}')
            try:
                keyword.check_candiates()
                if(hasattr(keyword, 'link_dictionary')):
                    DEFAULT_LINK_CHECKER.check_links(keyword.link_dictionary)
            except KeyError:
                print(f'[INTERNAL ERROR] {keyword.name} has failed')
                self.assertTrue(False)
            print(f'[INTERNAL SUCCESS] {keyword.name} has passed')
