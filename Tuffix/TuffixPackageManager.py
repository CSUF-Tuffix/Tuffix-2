import pathlib
import apt
from apt import auth
from aptsources import sourceslist
from aptsources.sourceslist import SourceEntry
import urllib.request
import re

from Tuffix.AbstractKeyword import AbstractKeyword
from Tuffix.PackageManager import BasePackageManager
from Tuffix.LinkChecker import LinkPacket
from Tuffix.SudoRun import SudoRun

class TuffixPackageManager(BasePackageManager):
    def __init__(self, path: pathlib.Path, managed_object):
        if not(issubclass(type(managed_object), AbstractKeyword)):
            raise ValueError(f'{type(managed_object).__name__}')
        super().__init__(path, managed_object)
        self.sources = sourceslist.SourcesList(True, "/etc/apt")
        self.valid_architectures = ["amd64", "arm64"]

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

    def _parse_source(self, line: str) -> tuple:
        """
        This is an undocumeted feature and I need to read the source code
        of this project get this to work. Debian...WRITE BETTER DOCS!
        """

        _entry = SourceEntry(line)
        _entry.parse(line)
        return (_entry.type,
                _entry.uri,
                _entry.dist,
                _entry.comps,
                _entry.architectures)

    def install_source(self, source: str):
        """
        Given repo source, as defined here:
        https://manpages.ubuntu.com/manpages/xenial/man5/sources.list.5.html
        """

        __type, uri, distrib, arguments, arch = self._parse_source(source)
        self.sources.add(__type, uri, distrib, arguments, architectures=arch)
        self.sources.save()

    def install_gpg_key(self, path: str):
        """
        Given either a link or direct path on disk,
        this function will read the contents and install the GPG key
        """

        _re = re.compile("(?P<link>((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)")
        contents = None
        if((match := _re.match(path))):
            contents = urllib.request.urlopen(match.group("link")).read()
        else:
            with open(path, "wb") as fp:
                contents = ''.join(fp.readlines())

        auth.add_key(contents.decode('utf-8'))

    # def _install_third_party(self, gpg_packet: LinkPacket, deb_source: str):
        # if not(isinstance(gpg_packet, LinkPacket) and
               # isinstance(deb_source, str)):
            # raise ValueError

        # """
        # This is a combination of the two functions below for easier use
        # """

        # self.install_source(deb_source)
        # self.install_gpg_key(gpg_packet.link)

    def install_third_party(self):
        _re  = re.compile(".*GPG.*")
        gpg_objects = []
        if(hasattr(self.managed_object, 'link_dictionary')):
            container = list(self.managed_object.link_dictionary.keys())
            _keys = list(filter(_re.match, container))
            gpg_objects = [self.managed_object.link_dictionary.get(_) for _ in _keys]

        for gpg in gpg_objects:
            self.install_gpg_key(gpg.link)
        if(hasattr(self.managed_object, 'repo_payload')):
            self.install_source(self.managed_object.repo_payload)
