from Tuffix.Configuration import *

import apt

class AbstractKeyword:
    """
    Keyword names may begin with a course code (digits), but Python
    identifiers may not. If a keyword name starts with a digit, prepend
    the class name with C (for Course).
    """

    def __init__(self, build_config, name, description, packages=None):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(name, str) and
                len(name) <= KEYWORD_MAX_LENGTH and
                isinstance(description, str)):
            raise ValueError
        self.name = name
        self.description = description
        self.packges: list[str] = [] if not packages else packages
        self.checkable_packages: list[str] = [] # should be set to nothing
        self.build_config = build_config

    def add(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def check_candiates(self):
        """
        Check all package candiates to see if they can be installed
        For unit testing
        """

        current_cache = apt.cache.Cache()
        current_cache.update()

        container = self.packages if not self.checkable_packages else self.checkable_packages
        print(container)

        for package in container:
            # will raise KeyError if not found
            try:
                _ = current_cache[package]
            except KeyError:
                current_cache.close()
                raise KeyError(f'could not find {package}')

        current_cache.close()
