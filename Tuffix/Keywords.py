##########################################################################
# keywords
# AUTHORS: Kevin Wortman, Jared Dyreson
##########################################################################

from Tuffix.AbstractKeyword import AbstractKeyword
# this is because we want to have access to this base class across two source files that import each other

from Tuffix.Editors import *

from Tuffix.Configuration import *
from Tuffix.SudoRun import SudoRun
from Tuffix.KeywordHelperFunctions import *
from Tuffix.Status import *

from apt import debfile, cache
from zipfile import ZipFile
import functools
import json
import requests
import sys


class AllKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(
            build_config,
            'all',
            'all keywords available (glob pattern); to be used in conjunction with remove or add respectively')
        self.packages = []

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class GeneralKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee
    SRC: sub-tuffix/min-tuffix.yml (Kitchen sink)
    """

    def __init__(self, build_config):
        super().__init__(
            build_config,
            'general',
            'General configuration, not tied to any specific course')
        self.packages = ['autoconf',
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
        edit_deb_packages(self.packages, is_installing=True)
        VimKeyword(self.build_config).add()
        EmacsKeyword(self.build_config).add()

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        VimKeyword(self.build_config).remove()
        EmacsKeyword(self.build_config).remove()


class BaseKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee
    TODO: we need to be in agreement to only used python3.5 or greater
    Python 2.7 is dead
    """

    def __init__(self, build_config):
        super().__init__(build_config,
                         'base',
                         'CPSC 120-121-131-301 C++ development environment')

        self.packages = ['build-essential',
                         'cimg-dev',
                         'clang',
                         'clang-format',
                         'clang-tidy',
                         'cmake',
                         'code',
                         'gdb',
                         'gcc',
                         'git',
                         'g++',
                         'libc++-dev',
                         'libc++abi-dev',
                         'libgconf-2-4',
                         'libgtest-dev',
                         'libgmock-dev',
                         'lldb',
                         'python2']

        self.link_dictionary = {
            "GOOGLE_TEST_URL": ["https://github.com/google/googletest.git", True],
            "TEST_URL": ["https://github.com/JaredDyreson/tuffix-google-test.git", True]
        }

    def add(self):
        self.google_test_all()
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)

    def google_test_build(self):
        """
        GOAL: Get and install GoogleTest
        """
        GOOGLE_TEST_URL = self.link_dictionary["GOOGLE_TEST_URL"][0]
        # GOOGLE_TEST_URL = "https://github.com/google/googletest.git"
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

    def google_test_attempt(self):
        """
        Goal: small test to check if Google Test works after install
        """
        # TODO : change link to be under CSUF domain
        # TEST_URL = "https://github.com/JaredDyreson/tuffix-google-test.git"
        TEST_URL = self.link_dictionary["TEST_URL"][0]
        TEST_DEST = "test"

        os.chdir("/tmp")
        if(os.path.isdir(TEST_DEST)):
            shutil.rmtree(TEST_DEST)
        subprocess.run(['git', 'clone', TEST_URL, TEST_DEST])
        os.chdir(TEST_DEST)
        subprocess.check_output(['clang++', '-v', 'main.cpp', '-o', 'main'])
        ret_code = subprocess.run(['make', 'all']).returncode
        if(ret_code != 0):
            print(colored("[ERROR] Google Unit test failed!", "red"))
        else:
            print(colored("[SUCCESS] Google unit test succeeded!", "green"))

    def google_test_all(self):
        """
        Goal: make and test Google Test library install
        """

        self.google_test_build()
        self.google_test_attempt()


class C223JKeyword(AbstractKeyword):

    """
    NOTE: do you want to use a newer version of Java?
    Or are the IDE's dependent on a certain version?

    Point Person: Floyd Holliday
    SRC: sub-tuffix/cpsc223j.yml
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C223J', 'CPSC 223J (Java Programming)')
        self.packages = ['geany',
                         'gthumb',
                         'netbeans',
                         'openjdk-8-jdk',
                         'openjdk-8-jre']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C223NKeyword(AbstractKeyword):
    """
    Point person: Floyd Holliday
    SRC: sub-tuffix/cpsc223n.yml
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C223N', 'CPSC 223N (C# Programming)')
        self.packages = ['mono-complete',
                         'netbeans']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C223PKeyword(AbstractKeyword):
    """
    python 2.7 and lower pip no longer exists
    has been superseeded by python3-pip
    also python-virtualenv no longer exists

    Python 3.8.5 is latest build

    Point person: Michael Shafae
    SRC: sub-tuffix/cpsc223p.yml
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C223P', 'CPSC 223P (Python Programming)')
        self.packages = ['python2',
                         'python2-dev',
                         # 'python-pip',
                         # 'python-virtualenv',
                         'python3',
                         'python3-dev',
                         'python3-pip',
                         'virtualenvwrapper']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C223WKeyword(AbstractKeyword):

    """
    Point person: Paul Inventado
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C223W', 'CPSC 223W (Swift Programming)')
        self.packages = ['binutils',
                         'curl',
                         'gnupg2',
                         'libc6-dev',
                         'libcurl4',
                         'libedit2',
                         'libgcc-9-dev',
                         'libpython2.7',
                         'libsqlite3-0',
                         'libstdc++-9-dev',
                         'libxml2',
                         'libz3-dev',
                         'pkg-config',
                         'tzdata',
                         'zlib1g-dev']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C240Keyword(AbstractKeyword):

    """
    Point person: Floyd Holliday
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C240', 'CPSC 240 (Assembler)')
        self.packages = ['intel2gas',
                         'nasm']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C351Keyword(AbstractKeyword):

    """
    Point person: William McCarthy
    """
    # TODO: testing and doing

    def __init__(self, build_config):
        super().__init__(build_config, 'C351', 'CPSC 351 (Operating Systems)')
        self.packages = [f'linux-headers-{current_kernel_revision()}']

    def add(self):
        print('important that you make a save state in your VM of tuffix or just install the tuffix installers scripts in another VM if you have a native install. You can mess up your main OS')
        edit_deb_packages(self.packages, is_installing=True)
        silberschatz_url = "http://cs.westminstercollege.edu/~greg/osc10e/final-src-osc10e.zip"
        r = requests.get(silberschatz_url)
        stored = "/tmp/kernel-exercises.zip"
        with open(stored, 'wb') as f:
            f.write(r.content)

        with ZipFile(stored, 'r') as zipObj:
            zipObj.extractAll()

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C439Keyword(AbstractKeyword):

    """
    Point person: <++>
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C439', 'CPSC 439 (Theory of Computation)')
        self.packages = ['minisat2']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C474Keyword(AbstractKeyword):

    """
    Point person: <++>
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C474', 'CPSC 474 (Parallel and Distributed Computing)')

        self.packages = ['libopenmpi-dev',
                         'mpi-default-dev',
                         'mpich',
                         'openmpi-bin',
                         'openmpi-common']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class C481Keyword(AbstractKeyword):

    """
    Java dependency is not installed by default
    Adding it so testing will work but needs to be addressed
    NOTE: usage of Java 8 should be discouraged

    Point person: Paul Inventado
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'C481', 'CPSC 481 (Artificial Intelligence)')
        self.packages = ['openjdk-8-jdk',
                         'openjdk-8-jre',
                         'sbcl',
                         'swi-prolog-nox',
                         'swi-prolog-x']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)
        EclipseKeyword(self.build_config).add()

    def remove(self):
        edit_deb_packages(packages, is_installing=False)
        EclipseKeyword(self.build_config).remove()


class C484Keyword(AbstractKeyword):

    """
    Point persons: Michael Shafae, Kevin Wortman
    Please note that python-openctm seems to not exist
    """

    # 'python-openctm']

    def __init__(self, build_config):
        super().__init__(build_config, 'C484', 'CPSC 484 (Principles of Computer Graphics)')
        self.packages = ['freeglut3-dev',
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
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class MediaKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(build_config, 'media', 'Media Computation Tools')
        self.packages = ['audacity',
                         'blender',
                         'gimp',
                         'imagemagick',
                         'sox',
                         'vlc']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class LatexKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(build_config,
                         'latex',
                         'LaTeX typesetting environment (large)')
        self.packages = ['texlive-full']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class VirtualBoxKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(
            build_config,
            'vbox',
            'A powerful x86 and AMD64/Intel64 virtualization product')
        self.packages = ['virtualbox',
                         'virtualbox-ext-pack']
        if(in_VM()):
            raise EnvironmentError(
                "This is a virtual enviornment, not proceeding")

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class ZoomKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(build_config,
                         'zoom',
                         'Video conferencing software')
        self.packages = ['libgl1-mesa-glx',
                         'libegl1-mesa',
                         'libxcb-xtest0',
                         'zoom']

        self.checkable_packages = self.packages[:3]

    def add(self):
        # print("[WARNING] Zoom is not an open source piece of software")
        edit_deb_packages(self.checkable_packages, is_installing=True)

        url = "https://zoom.us/client/latest/zoom_amd64.deb"
        file_path = "/tmp/zoom"
        with open(file_path, 'wb') as fp:
            fp.write(requests.get(url).content)
        apt.debfile.DebPackage(filename=file_path).install()

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)


class TestKeyword(AbstractKeyword):

    def __init__(self, build_config):
        super().__init__(build_config,
                         'test',
                         'for testing purposes [please remove when not needed]')

        self.packages = ['cowsay']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)
        VimKeyword(self.build_config).add()
        EmacsKeyword(self.build_config).add()

    def remove(self):
        # VimKeyword(self.bc).remove()
        # EmacsKeyword(self.bc).remove()
        edit_deb_packages(self.packages, is_installing=False)


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
            C439Keyword(build_config),
            C474Keyword(build_config),
            C481Keyword(build_config),
            C484Keyword(build_config),
            GeneralKeyword(build_config),
            LatexKeyword(build_config),
            MediaKeyword(build_config),
            TestKeyword(build_config),
            VirtualBoxKeyword(build_config),
            ZoomKeyword(build_config),
        ]

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


def partial_class(information: tuple, cls):
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

    name, description, packages = information

    body = {
        "__init__": functools.partialmethod(cls.__init__, build_config=DEFAULT_BUILD_CONFIG, name=name, description=description, packages=packages),
        "add": partial(edit_deb_packages, package_names=packages, is_installing=True),
        "remove": partial(edit_deb_packages, package_names=packages, is_installing=False)
    }

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
    BUG: there might be an issue in where the class is instantiated
    """

    def __init__(self):
        pass

    def generate(self, path: str):
        if not(isinstance(path, str)):
            raise ValueError

        if(not os.path.exists(path)):
            raise FileNotFoundError(f'could not load {path}')

        with open(path, encoding="utf-8") as fp:
            content = json.loads(fp.read())

        name, instructor, packages = content["name"].replace(
            ' ', '').lower(), content["instructor"], content["packages"]
        description = f'{name} created by {instructor}'

        return partial_class((name, instructor, packages), AbstractKeyword)


DEFAULT_CLASS_GENERATOR = ClassKeywordGenerator()
