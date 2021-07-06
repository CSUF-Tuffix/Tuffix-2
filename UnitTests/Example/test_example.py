import unittest


class ExampleTest(unittest.TestCase):
    def test_a(self):
        self.assertTrue(1 == 1)

    def test_b(self):
        self.assertTrue(1 != 0)

    def test_c(self):
        self.assertTrue(2 > 1)
