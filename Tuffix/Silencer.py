import sys
import contextlib
import apt

"""
Silence function output
Source: https://stackoverflow.com/a/2829036
"""


class DummyFile(object):
    def write(self, x): pass
    def flush(self): pass

@contextlib.contextmanager
def silence():
    _stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = _stdout

# Try to silence apt output
# Source: https://stackoverflow.com/a/24146012

class LogInstallProgress(apt.progress.base.InstallProgress):
    def fork(self):
        pid = os.fork()
        if pid == 0:
            logfd = os.open("dpkg.log", os.O_RDWR | os.O_APPEND | os.O_CREAT, 0o644)
            os.dup2(logfd, 1)
            os.dup2(logfd, 2)
        return pid
