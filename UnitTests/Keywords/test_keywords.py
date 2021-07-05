import unittest

from Tuffix.Keywords import KeywordContainer
from Tuffix.Editors import EditorKeywordContainer
from Tuffix.LinkChecker import DEFAULT_LINK_CHECKER


class KeywordTest(unittest.TestCase):
    def template(self, k_container):
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

    def test_editors(self):
        self.template(EditorKeywordContainer)

    def test_keywords(self):
        self.template(KeywordContainer)
