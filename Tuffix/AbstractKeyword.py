from Tuffix.Configuration import *

import apt
import pip


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
        self.packages: list[str] = [] if not packages else packages
        self.checkable_packages: list[str] = []  # should be set to nothing
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

        for package in container:
            # will raise KeyError if not found
            try:
                _ = current_cache[package]
            except KeyError:
                current_cache.close()
                raise KeyError(f'could not find {package}')

        current_cache.close()

    def is_deb_package_installed(self, package_name: str) -> bool:
        if not(isinstance(package_name, str)):
            raise ValueError(f'{package_name=} expected to be `str`')
        try:
            apt.apt_pkg.init()
            cache = apt.apt_pkg.Cache(None)  # quiet this output for testing
            package = cache[package_name]
            return (package.current_state == apt.apt_pkg.CURSTATE_INSTALLED)
        except KeyError:
            raise EnvironmentError(
                f'[ERROR] No such package "{package_name}"; is this Ubuntu?')

    @classmethod
    def edit_deb_packages(self, package_names: list, is_installing: bool):
        if not (isinstance(package_names, list) and
                all(isinstance(name, str) for name in package_names) and
                isinstance(is_installing, bool)):
            raise ValueError
        print(
            f'[INFO] Adding all packages to the APT queue ({len(package_names)})')
        cache = apt.cache.Cache()
        cache.update()
        cache.open()

        for name in package_names:
            print(
                f'[INFO] {"Installing" if is_installing else "Removing"} package: {name}')
            try:
                cache[name].mark_install() if(
                    is_installing) else cache[name].mark_delete()
            except KeyError:
                raise EnvironmentError(
                    f'[ERROR] Debian package "{name}" not found, is this Ubuntu?')
        try:
            cache.commit()
        except OSError:
            DEFAULT_PROCESS_HANDLER.remove_process("apt")
            raise EnvironmentError(
                '[FATAL] Could not continue, apt was holding resources. Processes were killed, please try again.')
        except Exception as e:
            cache.close()
            raise EnvironmentError(f'[ERROR] Could not install {name}: {e}.')
        finally:
            # unittest complains there is an open file but I have tried closing it in every avenue
            # NOTE : possible memory leak
            cache.close()

    def install_pip_packages(self, packages: list):
        if not(isinstance(packages, list)):
            raise ValueError
        for package in packages:
            pip.main(['install', package])
