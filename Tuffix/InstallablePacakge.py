import apt
import platform
# MARK FOR REMOVAL
# from Tuffix.LSBParsr import lsb_parser

class Cache:
    def __init__(self):
        self.current_cache = apt.cache.Cache()
        self.update()

    def update(self):
        self.current_cache.update()

    def __del__(self):
        self.current_cache.close()


DEFAULT_CACHE = Cache()

class PackageContainer:
    def __init__(self, packages: list):
        if not(isinstance(packages, list) and
               all([isinstance(_, str) for _ in packages])):
               raise ValueError(f'expected list[str]')

        self.packages = packages
        self.architecture = platform.machine()
        # self.l_parser = lsb_parser()

    def ensure_installable(self):
        """
        Check all package candiates to see if they can be installed
        For unit testing
        """

        for package in self.packages:
            # will raise KeyError if not found
            _ = DEFAULT_CACHE.current_cache[package]

container = PackageContainer(['atom', 'cowsay'])
container.ensure_installable()
