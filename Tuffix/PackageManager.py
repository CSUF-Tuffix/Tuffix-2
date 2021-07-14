import pathlib

class BasePackageManager:
    def __init__(self, path: str, managed_object=None, secondary_manager=None):
        # if not(isinstance(path, str)):
            # raise ValueError
        """
        path: absolute path to the binary used
        managed_object: objects that should be controlled using a PackageManager
                        For example: Tuffix/Keyword.py
        secondary_manager: if the target system has another package manager to handle building packages from source
                           please use this. For example: Arch Linux
        """

        self.path = path
        self.managed_object = managed_object
        self.secondary_manager = secondary_manager

    def install(self, package: str):
        """
        Install a package from the sancitioned
        repositories on your system
        """
        if not(isinstance(package, str)):
            raise ValueError(
                f'expected `str`, obtained {type(package).__name__}')

    def remove(self, package: str):
        """
        Remove a package from the sancitioned
        repositories on your system
        """
        if not(isinstance(package, str)):
            raise ValueError(
                f'expected `str`, obtained {type(package).__name__}')

    def install_bulk(self, packages: list):
        if not(isinstance(packages, list) and
               all([isinstance(_, str) for _ in packages])):
            raise ValueError(
                f'expected list[str], obtained {type(packages).__name__}')

        for pkg in packages:
            self.install(pkg)

    def install_from_file(self, path: pathlib.Path):
        """
        Install package from a local file
        """
        if not((istype := isinstance(path, pathlib.Path)) and
               (is_present := path.is_file())):
            raise ValueError(f'istype: {istype} and is_present: {is_present}')

    def update_cache(self) -> None:
        """
        Rebuild the cache of packages you can install
        """

        raise NotImplementedError

    def build_installed_cache(self) -> None:
        """
        Get a dictionary of PackageInstance objects
        """
        raise NotImplementedError

    def list_installed(self, foreign: bool = False):
        """
        List the packages installed on the system
            foreign: packages built using another package manager such as `yay` or `yaourt`
        """
        raise NotImplementedError

    def _candidate_installable(self, package: str):
        """
        Note: helper function to check_candiates
        """

        raise NotImplementedError

    def check_candiates(self, packages: list):
        """
        Check a list of packages to be installed on a machine
        """

        raise NotImplementedError

    def install_source(self, string: tuple):
        """
        Install a repository on the target machine
        """

        raise NotImplementedError

    def install_gpg_key(self, path: str):
        """
        Install gpg key on machine
        Example: apt-key add [PATH]
        Targets Debian machines mostly
        """
        raise NotImplementedError

    def check_if_installed(self, package: str):
        raise NotImplementedError

