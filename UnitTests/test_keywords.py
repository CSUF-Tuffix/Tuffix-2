import unittest

from Tuffix.Keywords import *
from Tuffix.Constants import *

class KeywordTest(unittest.TestCase):
    def test_availability(self):
        """
        Ensure all the packages are available
        on a given platform
        """
        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)

        for keyword in k_container.container:
            print(f'checking {keyword.name}')
            try:
                keyword.check_candiates()
            except KeyError:
                print(f'[INTERNAL ERROR] {keyword.name} has failed')
                self.assertTrue(False)
            print(f'[INTERNAL SUCCESS] {keyword.name} has passed')
