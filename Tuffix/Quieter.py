import sys
import contextlib

from io import StringIO
import sys

"""
Silence function output
Source: https://stackoverflow.com/a/2829036
"""


class DummyFile(object):
    def write(self, x): pass
    def flush(self): pass


@contextlib.contextmanager
def quiet():
    _stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = _stdout

# Capture the output of a function
# Source : https://stackoverflow.com/a/16571630


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class CapturingStderr(list):
    def __enter__(self):
        self._stderr = sys.stderr
        sys.stderr = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stderr = self._stderr
