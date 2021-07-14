import pathlib
import apt

from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.PackageManager import BasePackageManager

class TuffixPackageManager(BasePackageManager):
    def __init__(self, path: pathlib.Path, managed_object: AbstractKeyword):
        if not(issubclass(type(managed_object), AbstractKeyword)):
            raise ValueError(f'{type(managed_object).__name__}')
        super().__init__(path, managed_object)

    def _edit_package_state(self, packages: list, is_installing: bool):
        """
        Internal helper function for install and remove
        """
        cache = apt.cache.Cache()
        verb = "Installing" if is_installing else "Removing"

        with cache.actiongroup():
            for pkg in packages:
                candidate = cache.get(pkg)
                if(isinstance(candidate, type(None))):
                    raise EnvironmentError(f'[ERROR] Could not find the package {pkg}, is this Ubuntu?')
                print(f'[INFO] {verb} package: {pkg}')
                candidate.mark_install() if(
                    is_installing) else candidate.mark_delete()
            """
            https://salsa.debian.org/apt-team/python-apt/-/blob/main/apt/cache.py#L640
            This will most likely change in the future
            """

            result = cache.commit()
            if not(result):
                for pkg in packages:
                    _is_installed = self.check_if_installed(pkg)
                    print(f'[INFO] Package: {pkg}, Installed: {_is_installed}')
                raise EnvironmentError(f'[ERROR] Could not successfully complete ttask')

    def install(self, package: str):
        super().install(package)
        self._edit_package_state(packages=[package], is_installing=True)

    def remove(self, package: str):
        super().remove(package)
        self._edit_package_state(packages=[package], is_installing=False)

    def install_bulk(self, packages: list):
        for pkg in packages:
            self.install(pkg)

    def install_all_candidates(self):
        """
        Install all packages from the managed_object
        """

        self.install_bulk(self.managed_object.packages)

    def check_all_candidates(self) -> bool:
        """
        Check if all the packages successfully install
        """

        return all([self.check_if_installed(pkg) for pkg in self.managed_object.packages])

    def check_if_installed(self, package: str) -> bool:
        apt.apt_pkg.init()
        cache = apt.apt_pkg.Cache(None)
        candiate = cache[package]
        return (candiate.current_state == apt.apt_pkg.CURSTATE_INSTALLED)


    def install_from_file(self, path: pathlib.Path):
        """
        Install a valid package on disk
        """

        super().install_from_file(path)
        apt.debfile.DebPackage(filename=str(path)).install()

