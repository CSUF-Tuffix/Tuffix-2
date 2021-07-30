"""
keywords
AUTHORS: Kevin Wortman, Jared Dyreson
"""

from Tuffix.AbstractKeyword import AbstractKeyword
# this is because we want to have access to this base class across two
# source files that import each other

from Tuffix.Editors import VimKeyword, EmacsKeyword, GeanyKeyword, NetbeansKeyword, EditorKeywordContainer, AtomKeyword, EclipseKeyword, BlankEditorKeyword

from Tuffix.Configuration import *
from Tuffix.SudoRun import SudoRun
from Tuffix.Status import *
from Tuffix.LinkChecker import LinkPacket
from Tuffix.Constants import KEYWORD_MAX_LENGTH

from Tuffix.CustomPayload import CustomPayload

from zipfile import ZipFile

import functools
import json
import pathlib
import requests
import sys
import dataclasses
import os


class AllKeyword(AbstractKeyword):
    # NOTE: GOOD

    def __init__(self, build_config: BuildConfig):
        super().__init__(
            build_config,
            'all',
            'all keywords available (glob pattern); to be used in conjunction with remove or add respectively')
        self.packages: list[str] = []

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class GeneralKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee
    SRC: sub-tuffix/min-tuffix.yml (Kitchen sink)

    - removed EmacsKeyword
    """

    # NOTE: GOOD

    def __init__(self, build_config: BuildConfig):
        super().__init__(
            build_config,
            'general',
            'General configuration, not tied to any specific course')
        self.packages: list[str] = ['autoconf',
                                    'automake',
                                    'a2ps',
                                    'cscope',
                                    'curl',
                                    'dkms',
                                    'enscript',
                                    'glibc-doc',
                                    'gpg',
                                    'graphviz',
                                    'gthumb',
                                    'libreadline-dev',
                                    'manpages-posix',
                                    'manpages-posix-dev',
                                    'meld',
                                    'nfs-common',
                                    'openssh-client',
                                    'openssh-server',
                                    'seahorse',
                                    'synaptic']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        VimKeyword(self.build_config).add()

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        VimKeyword(self.build_config).remove()


class ClangKeyword(AbstractKeyword):

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'clang',
                         'clang temp')
        self.repo_payload = "ppa:ubuntu-toolchain-r/test"
        self.packages: list[str] = ['clang-12',
                                    'clang-12-doc',
                                    'clang-format-12',
                                    'clang-tidy-12',
                                    'clang-tools-12',
                                    'clangd-12',
                                    'g++-11',
                                    'gcc-11',
                                    'libc++-12-dev',
                                    'libc++abi-12-dev'
                                    'libclang-12-dev',
                                    'libclang-common-12-dev',
                                    'libclang1-12',
                                    'lld-12',
                                    'lldb-12',
                                    'python3-clang-12']

    def update_alternative(self, link: str, name: str, path: pathlib.Path, priority: int, slave_components):
        for slave in slave_components:
            slave_link, slave_name, slave_path = slave
            os.system(
                f"update-alternatives --install {link} {name} {path} {priority} --slave {slave_link} {slave_name} {slave_path}")

    def install_ppa(self):
        self.write_to_sources(self.repo_payload, True)

    def link_all_binaries(self):
        _gcc_11 = [
            ('/usr/bin/g++',         'g++',         '/usr/bin/g++-11'),
            ('/usr/bin/gcc-ar',      'gcc-ar',      '/usr/bin/gcc-ar-11'),
            ('/usr/bin/gcc-nm',      'gcc-nm',      '/usr/bin/gcc-nm-11'),
            ('/usr/bin/gcc-ranlib',  'gcc-ranlib',  '/usr/bin/gcc-ranlib-11'),
            ('/usr/bin/gcov',        'gcov',        '/usr/bin/gcov-11'),
            ('/usr/bin/gcov-dump',   'gcov-dump',   '/usr/bin/gcov-dump-11'),
            ('/usr/bin/gcov-tool',   'gcov-tool',   '/usr/bin/gcov-tool-11')
        ]

        _gcc_9 = [
            ('/usr/bin/g++',         'g++',         '/usr/bin/g++-9'),
            ('/usr/bin/gcc-ar',      'gcc-ar',      '/usr/bin/gcc-ar-9'),
            ('/usr/bin/gcc-nm',      'gcc-nm',      '/usr/bin/gcc-nm-9'),
            ('/usr/bin/gcc-ranlib',  'gcc-ranlib',  '/usr/bin/gcc-ranlib-9'),
            ('/usr/bin/gcov',        'gcov',        '/usr/bin/gcov-9'),
            ('/usr/bin/gcov-dump',   'gcov-dump',   '/usr/bin/gcov-dump-9'),
            ('/usr/bin/gcov-tool',   'gcov-tool',   '/usr/bin/gcov-tool-9')
        ]

        _clang_12 = [
            ('/usr/bin/clang++'            'clang++'            '/usr/bin/clang++-12'),
            ('/usr/bin/clang-format'       'clang-format'       '/usr/bin/clang-format-12'),
            ('/usr/bin/clang-format-diff'  'clang-format-diff'  '/usr/bin/clang-format-diff-12'),
            ('/usr/bin/clang-tidy'         'clang-tidy'         '/usr/bin/clang-tidy-12'),
            ('/usr/bin/clang-tidy-diff'    'clang-tidy-diff'    '/usr/bin/clang-tidy-diff-12.py')
        ]

        _clang_10 = [
            ('/usr/bin/clang++',            'clang++',
             '/usr/bin/clang++-10'),
            ('/usr/bin/clang-format',       'clang-format',
             '/usr/bin/clang-format-10'),
            ('/usr/bin/clang-format-diff',  'clang-format-diff',
             '/usr/bin/clang-format-diff-10'),
            ('/usr/bin/clang-tidy',         'clang-tidy',
             '/usr/bin/clang-tidy-10'),
            ('/usr/bin/clang-tidy-diff',    'clang-tidy-diff',
             '/usr/bin/clang-tidy-diff-10.py')
        ]
        self.update_alternative('/usr/bin/gcc', 'gcc',
                                '/usr/bin/gcc-11', 11, _gcc_11)
        self.update_alternative('/usr/bin/gcc', 'gcc',
                                '/usr/bin/gcc-9', 9, _gcc_9)
        self.update_alternative('/usr/bin/clang', 'clang',
                                '/usr/bin/clang-12', 12, _clang_12)
        self.update_alternative('/usr/bin/clang', 'clang',
                                '/usr/bin/clang-10', 10, _clang_10)

    def add(self):
        # self.edit_deb_packages(self.packages, is_installing=True)
        self.install_ppa()

    def remove(self):
        # self.edit_deb_packages(self.packages, is_installing=False)
        pass


class BaseKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee

    - removed python2, this has been discarded in favour of python3.8
    - removed vscode from list of packages, this keyword already installs Atom
    - updated clang => clang-12
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'base',
                         'CPSC 120-121-131-301 C++ development environment')

        self.packages: list[str] = ['autoconf',
                                    'automake',
                                    'build-essential',
                                    'cimg-dev',
                                    'clang',
                                    'clang-format',
                                    'clang-tidy',
                                    'cmake',
                                    'gdb',
                                    'gcc',
                                    'git',
                                    'googletest',
                                    'g++',
                                    'libc++-dev',
                                    'libc++abi-dev',
                                    'libgconf-2-4',
                                    'libgtest-dev',
                                    'libgmock-dev',
                                    'lldb',
                                    'nlohmann-json3-dev',
                                    'subversion',
                                    'python3']

        self.Atom = AtomKeyword(self.build_config)
        self.repo_payload = "ppa:ubuntu-toolchain-r/test"

        self.link_dictionary = {
            "GOOGLE_TEST_URL": LinkPacket(
                link="https://github.com/google/googletest.git",
                is_git=True),
            "TEST_URL": LinkPacket(
                link="https://github.com/JaredDyreson/tuffix-google-test.git",
                is_git=True)}

    def add(self):
        self.build_google_test()
        self.edit_deb_packages(self.packages, is_installing=True)
        self.Atom.add()

    def remove(self):
        # self.edit_deb_packages(self.packages, is_installing=False)
        self.Atom.remove()

    def build_google_test(self):
        """
        GOAL: Get and install GoogleTest
        NOTE: does this need to be done? <- can `googletest` from Ubuntu repos do this for us?
        Test with clean version of Ubuntu
        """

        GOOGLE_TEST_URL = self.link_dictionary["GOOGLE_TEST_URL"].link
        GOOGLE_DEST = "google"

        os.chdir("/tmp")
        if(os.path.isdir(GOOGLE_DEST)):
            shutil.rmtree(GOOGLE_DEST)
        subprocess.run(['git', 'clone', GOOGLE_TEST_URL, GOOGLE_DEST])
        os.chdir(GOOGLE_DEST)
        script = ["cmake CMakeLists.txt",
                  "make -j8",
                  "sudo cp -r -v googletest/include/. /usr/include",
                  "sudo cp -r -v googlemock/include/. /usr/include",
                  "sudo chown -v root:root /usr/lib"]
        for command in script:
            subprocess.run(command.split())


class BazelKeyword(AbstractKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(
            build_config,
            'bazel',
            'software tool that allows for the automation of building and testing of software')
        self.packages: list[str] = ['curl',
                                    'gnupg',
                                    'bazel']
        self.checkable_packages = self.packages[:-1]
        self.link_dictionary = {
            "BAZEL_GPG": LinkPacket(
                link="https://bazel.build/bazel-release.pub.gpg",
                is_git=False)}
        self.repo_payload = "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8"

    def add(self):
        pass
        # gpg_url = self.link_dictionary["BAZEL_GPG"].link
        # gpg_dest = pathlib.Path("/tmp/gpgkey")

        # content = requests.get(gpg_url).content

        # with open(gpg_dest, "wb") as fp:
        # fp.write(content)

        # self.executor.run(
        # f'sudo apt-key add {gpg_dest.resolve()}',
        # self.executor.whoami)

        # self.write_to_sources(self.repo_payload, True)  # please depreciate
        # self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class C223JKeyword(AbstractKeyword):

    """
    NOTE: do you want to use a newer version of Java?
    Or are the IDE's dependent on a certain version?

    Point Person: Floyd Holliday
    SRC: sub-tuffix/cpsc223j.yml

    - removed geany, netbeans from self.packages
    - moved them to EditorKeyword instead
    - we need to make a decision which editor to use, both are going to be installed
      to appease the Gods
    - updated from Java version 8 to 11
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '223J', 'CPSC 223J (Java Programming)')
        self.packages: list[str] = ['gthumb',
                                    'openjdk-11-jdk',
                                    'openjdk-11-jre']
        self.Geany = GeanyKeyword(DEFAULT_BUILD_CONFIG)
        self.Netbeans = NetbeansKeyword(DEFAULT_BUILD_CONFIG)

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.Geany.add()
        self.Netbeans.add()

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.Geany.remove()
        self.Netbeans.remove()


class C223NKeyword(AbstractKeyword):
    """
    Point person: Floyd Holliday
    SRC: sub-tuffix/cpsc223n.yml
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         '223N', 'CPSC 223N (C# Programming)')
        self.packages: list[str] = ['mono-complete']
        self.Netbeans = NetbeansKeyword(DEFAULT_BUILD_CONFIG)

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.Netbeans.add()

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.Netbeans.remove()


class C223PKeyword(AbstractKeyword):
    """
    Point person: Michael Shafae
    SRC: sub-tuffix/cpsc223p.yml
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '223P', 'CPSC 223P (Python Programming)')
        self.packages: list[str] = ['build-essential',
                                    'libssl-dev',
                                    'libffi-dev',
                                    'python3',
                                    'python3-dev',
                                    'python3-pip',
                                    'virtualenvwrapper']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.install_pip_packages(["virtualenv"])

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class C223WKeyword(AbstractKeyword):

    """
    Point person: Paul Inventado
    - removed libpython2.7, replaced wtih libpython3.8
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '223W', 'CPSC 223W (Swift Programming)')
        self.packages: list[str] = ['binutils',
                                    'curl',
                                    'gnupg2',
                                    'libc6-dev',
                                    'libcurl4',
                                    'libedit2',
                                    'libgcc-9-dev',
                                    'libpython3.8',
                                    'libsqlite3-0',
                                    'libstdc++-9-dev',
                                    'libxml2',
                                    'libz3-dev',
                                    'pkg-config',
                                    'tzdata',
                                    'zlib1g-dev']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class C240Keyword(AbstractKeyword):

    """
    Point person: Floyd Holliday
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '240', 'CPSC 240 (Assembler)')
        self.packages: list[str] = ['intel2gas', 'nasm']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class C474Keyword(AbstractKeyword):

    """
    Point person: <++>
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '474', 'CPSC 474 (Parallel and Distributed Computing)')

        self.packages: list[str] = ['libopenmpi-dev',
                                    'mpi-default-dev',
                                    'mpich',
                                    'openmpi-bin',
                                    'openmpi-common']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class C481Keyword(AbstractKeyword):

    """
    Java dependency is not installed by default
    Adding it so testing will work but needs to be addressed
    NOTE: usage of Java 8 should be discouraged

    - removed openjdk-8 and replaced with openjdk-11
    - unknown if Eclipse is needed

    Point person: Paul Inventado
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '481', 'CPSC 481 (Artificial Intelligence)')
        self.packages: list[str] = ['openjdk-11-jdk',
                                    'openjdk-11-jre',
                                    'sbcl',
                                    'swi-prolog-nox',
                                    'swi-prolog-x']

        self.Eclipse = EclipseKeyword(self.build_config)

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.Eclipse.add()

    def remove(self):
        self.edit_deb_packages(packages, is_installing=False)
        self.Eclipse.remove()


class C484Keyword(AbstractKeyword):

    """
    Point persons: Michael Shafae, Kevin Wortman
    Please note that python-openctm seems to not exist

    - removed python-openctm
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, '484', 'CPSC 484 (Principles of Computer Graphics)')
        self.packages: list[str] = ['freeglut3-dev',
                                    'libfreeimage-dev',
                                    'libgl1-mesa-dev',
                                    'libglew-dev',
                                    'libglu1-mesa-dev',
                                    'libopenctm-dev',
                                    'libx11-dev',
                                    'libxi-dev',
                                    'libxrandr-dev',
                                    'mesa-utils',
                                    'mesa-utils-extra',
                                    'openctm-doc',
                                    'openctm-tools']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class MediaKeyword(AbstractKeyword):

    """
    Audacity is marked for removal, there has been some privacy concerns
     - 'audacity',
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'media', 'Media Computation Tools')
        self.packages: list[str] = ['blender',
                                    'gimp',
                                    'imagemagick',
                                    'sox',
                                    'vlc']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class LatexKeyword(AbstractKeyword):
    """
    Not for users, might have the same fate as AddRemoveHelper
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'latex',
                         'LaTeX typesetting environment (large)')
        self.packages: list[str] = ["texlive-full"]

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class GithubCLIKeyword(AbstractKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'gh',
                         'Github CLI utility')
        self.packages: list[str] = ["dirmngr",
                                    "software-properties-common",
                                    "gh"]
        self.checkable_packages: list[str] = self.packages[:-1]
        self.repo_payload = "https://cli.github.com/packages"

    def add(self):
        pass
        # if not((apt_key := shutil.which("apt-key"))):
        # raise EnvironmentError(f'could not find  {apt_key=}')
        # self.executor.run(
        # f'{apt_key} adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0',
        # self.executor.whoami)  # please depreciate

        # self.write_to_sources(self.repo_payload, True)  # please depreciate
        # self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class VirtualBoxKeyword(AbstractKeyword):

    def __init__(self, build_config: BuildConfig):
        super().__init__(
            build_config,
            'vbox',
            'A powerful x86 and AMD64/Intel64 virtualization product')
        self.packages: list[str] = ['virtualbox',
                                    'virtualbox-ext-pack']

        if(in_VM()):
            raise EnvironmentError(
                "This is a virtual enviornment, not proceeding")

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class ZoomKeyword(AbstractKeyword):
    """
    Note: imported deps from tuffix.yml @ https://github.com/mshafe/tuffix
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'zoom',
                         'Video conferencing software')
        self.packages: list[str] = ['libglib2.0-0',
                                    'libgstreamer-plugins-base0.10-0',
                                    'libxcb-shape0',
                                    'libxcb-shm0',
                                    'libxcb-xfixes0',
                                    'libxcb-randr0',
                                    'libxcb-image0',
                                    'libfontconfig1',
                                    'libgl1-mesa-glx',
                                    'libxi6',
                                    'libsm6',
                                    'libxrender1',
                                    'libpulse0',
                                    'libxcomposite1',
                                    'libxslt1.1',
                                    'libsqlite3-0',
                                    'libxcb-keysyms1',
                                    'libxcb-xtest0',
                                    'ibus',
                                    'zoom']
        self.checkable_packages = self.packages[:-1]
        self.link_dictionary = {
            "ZOOM_DEB": LinkPacket(
                link="https://zoom.us/client/latest/zoom_amd64.deb",
                is_git=False)}

    def add(self):
        pass
        # self.edit_deb_packages(self.checkable_packages, is_installing=True)

        # url = self.link_dictionary["ZOOM_DEB"].link
        # file_path = "/tmp/zoom"
        # print("[INFO] Downloading Zoom installer...")
        # content = requests.get(url).content

        # with open(file_path, 'wb') as fp:
        # fp.write(content)
        # apt.debfile.DebPackage(filename=file_path).install()

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)


class TMuxKeyword(AbstractKeyword):

    """
    Used for testing purposes as it only installs
    one package from APT
    Please use for debugging
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config,
                         'tmux',
                         'multi-tasking in the terminal')

        self.packages: list[str] = ['tmux']
        self.Blank = BlankEditorKeyword(self.build_config)

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.Blank.add()

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.Blank.remove()


class KeywordContainer():
    def __init__(self, build_config: BuildConfig):
        if(not isinstance(build_config, BuildConfig)):
            raise ValueError(
                f'expected BuildConfig for first argument, received: {type(build_configuration)}')
        self.container: list[AbstractKeyword] = [
            AllKeyword(build_config),
            BaseKeyword(build_config),
            C223JKeyword(build_config),
            C223NKeyword(build_config),
            C223PKeyword(build_config),
            C223WKeyword(build_config),
            C240Keyword(build_config),
            C474Keyword(build_config),
            C481Keyword(build_config),
            C484Keyword(build_config),
            ClangKeyword(build_config),
            GeneralKeyword(build_config),
            LatexKeyword(build_config),
            MediaKeyword(build_config),
            TMuxKeyword(build_config),
            VirtualBoxKeyword(build_config),
            ZoomKeyword(build_config),
        ]

        __container = EditorKeywordContainer(build_config).container
        self.container.extend(__container)

    def obtain(self, value: str) -> tuple:
        if(not isinstance(value, str)):
            raise ValueError(f'incorrect type: {type(value)}')

        for keyword in self.container:
            if(keyword.name == value):
                return (True, keyword)
        return (False, None)

    def __contains__(self, value: str):
        if(not isinstance(value, str)):
            raise ValueError(f'incorrect type: {type(value)}')

        _, status = self.obtain(value)
        return status


def partial_class(information: tuple, cls, build_config: BuildConfig):
    """
    Generate a valid function pointer to a class __init__ function
    This class is also pickle-able
    https://stackoverflow.com/a/58039373
    """

    if(not isinstance(information, tuple)):
        raise ValueError(f'exepecting tuple, received {type(name).__name__}')

    """
    Python 3.10 implementation for sanity checks
    match information:
        case [name, description, packages]:
            pass
        case _:
            raise FormattingError('expecting (name, description, packages)')
    """

    # will raise a ValueError if insufficient args given
    name, description, packages = information

    body = {
        "__init__": functools.partialmethod(
            cls.__init__,
            build_config=build_config,
            name=name,
            description=description,
            packages=packages),
        "add": functools.partial(
            cls.edit_deb_packages,
            package_names=packages,
            is_installing=True),
        "remove": functools.partial(
            cls.edit_deb_packages,
            package_names=packages,
            is_installing=False)}

    __class = type(name, (cls, ), body)

    try:
        __class.__module__ = sys._getframe(
            1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return __class


class ClassKeywordGenerator():
    """
    Generate a custom keyword class for usage in add/remove commands
    """

    def __init__(self):
        pass

    def generate(self, path: pathlib.PosixPath, build_config: BuildConfig):
        if not(isinstance(path, pathlib.PosixPath)):
            raise ValueError(f'received type {type(path).__name__}')

        if(not path.is_file()):
            raise FileNotFoundError(f'could not load {path}')

        with open(path, encoding="utf-8") as fp:
            content = json.loads(fp.read())

        __custom = CustomPayload(content)

        return partial_class(
            (__custom.name,
             f'created by {__custom.instructor} for {__custom.name}',
             __custom.packages),
            AbstractKeyword,
            build_config)


DEFAULT_CLASS_GENERATOR = ClassKeywordGenerator()
