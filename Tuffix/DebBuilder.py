import os
import pathlib
import re
import shutil
import tarfile
import textwrap

from Tuffix.Exceptions import ParsingError


class DebBuilder:
    """
    Take a tar ball and convert it to a Debian installer
    Similar to this: https://wiki.archlinux.org/title/PKGBUILD
    However with a lot less bells and whistles
    """

    def __init__(self, name: str, payload: pathlib.Path):
        if not(isinstance(payload, pathlib.Path) and
               isinstance(name, str)):
            raise ValueError
        self.name = name
        self.payload = payload
        _re_control = """
        Package: (?P<package>\\w+)
        Version: (?P<version>.*)
        Section: (?P<section>\\w+)
        Priority: (?P<severity>\\w+)
        Architecture: (?P<arch>[a-zA-Z0-9]+)
        Maintainer: (?P<maintainer>[a-zA-Z]+)\\s*?([<](?P<email>.*)[>])*
        Description: (?P<description>.*)
        Depends: *(?P<list>([a-zA-Z0-9\\-]+)(,\\s*[a-zA-Z0-9\\-]+)*)
        """
        self.control_re = re.compile(textwrap.dedent(_re_control).strip())

    def parse_control_file(self, control: pathlib.Path):
        """
        Goal: ensure the control file has a proper format
        """

        if not(isinstance(control, pathlib.Path)):
            raise ValueError(
                f'expecting pathlib.Path, obtained {type(control).__name__}')

        with open(control, "r") as fp:
            contents = ''.join(fp.readlines())
        _match = self.control_re.match(contents)

        if(not _match):
            raise ParsingError('control filed parsing')

        self.parsed_contents = _match

    def make_structure(self, children: list):
        """
        Goal: create the directory structure for the Debian package
        """

        if not(isinstance(children, list) and
               all([isinstance(_, pathlib.Path) for _ in children])):
            raise ValueError(f'expected list[pathlib.Path]')

        self.output = pathlib.Path(f'/tmp/{self.name}')
        self.output.mkdir(parents=True, exist_ok=True)
        for child in children:
            (self.output / child).mkdir(parents=True, exist_ok=True)

    def make(
            self,
            control: pathlib.Path,
            scripts=[],
            base_dir=[pathlib.Path('usr')],
            children=[]):
        if not(isinstance(control, pathlib.Path) and
               isinstance(scripts, list) and
               isinstance(base_dir, list) and
               all([isinstance(path, pathlib.Path) for path in base_dir]) and
               isinstance(children, list)):
            raise ValueError

        self.parse_control_file(control)  # can raise ParsingError

        base_dir.insert(0, pathlib.Path('DEBIAN'))

        self.make_structure(children)

        with tarfile.open(self.payload) as tar:
            # dump contents of tar into base dir
            tar.extractall(self.output / base_dir[0])

        debian_base = pathlib.Path(f'/tmp/{self.name}/DEBIAN')
        shutil.copy(control, (debian_base / 'control'))

        for script in scripts:
            if not(isinstance(script, pathlib.Path)):
                raise ValueError(
                    f'could not use {script} as script, not pathlib.Path')
            if(script.exists()):
                destination = debian_base / script.stem
                shutil.copy(script, destination)
                destination.chmod(0o775)  # give proper permissions
        self.debian_path = pathlib.Path(f'/tmp/{self.name}.deb')
        os.system(
            f'dpkg-deb --build {self.output} {self.debian_path}')
