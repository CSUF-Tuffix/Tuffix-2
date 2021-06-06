import unittest

class BaseUnitTest:
    def __init__(self, test: unittest.TestCase):
        if not(isinstance(test, unittest.TestCase)):
            # raise ValueError
            pass
        self.test = test
        ln = lambda f: getattr(self.test, f).func_code.co_firstlineno
        lncmp = lambda _, a, b: self._cmp(ln(a), ln(b))
        unittest.TestLoader.sortTestMethodsUsing = lncmp

    def run(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(self.test)
        unittest.TextTestRunner(failfast=True).run(suite)

    def _cmp(self, a, b) -> int:
        if(a < b):
            return 1
        if(a > b):
            return -1
        return 0
