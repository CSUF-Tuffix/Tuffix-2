"""
editors
AUTHOR: Jared Dyreson

Supported:
- atom
- eclipse
- emacs
- geany
- netbeans
- vi(m)
- vscode
"""

from Tuffix.Keywords import AbstractKeyword
from Tuffix.LinkChecker import LinkPacket

from Tuffix.SudoRun import SudoRun
from Tuffix.Exceptions import *
from Tuffix.Configuration import *
from Tuffix.DebBuilder import DebBuilder

import apt
import os
import pathlib
import requests
import subprocess
import shutil
import tarfile
import textwrap


class EditorBaseKeyword(AbstractKeyword):
    def __init__(self, build_config: BuildConfig, name: str, description: str):
        super().__init__(build_config, name, description)
        self.build_config = build_config
        self.executor = SudoRun()

    def update_state(self, arguments: list, install=True):
        """
        Goal: update the state file
        """

        if not(isinstance(arguments, list) and
               isinstance(install, bool)):
            raise ValueError

        current_state = read_state(self.build_config)

        new_action = current_state.editors

        for argument in arguments:
            if(not install):
                new_action.remove(argument)
            else:
                new_action.append(argument)

        new_state = State(self.build_config,
                          self.build_config.version,
                          current_state.installed,
                          new_action)
        new_state.write()


class AtomKeyword(EditorBaseKeyword):

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'atom', 'Github\'s own editor')
        self.packages: list[str] = ['atom']
        self.checkable_packages = []

        self.link_dictionary = {
            "ATOM_GPG_URL": LinkPacket(
                link="https://packagecloud.io/AtomEditor/atom/gpgkey",
                is_git=False)}

        self.file_footprint = {
            "ATOM_SOURCE": pathlib.Path("/etc/apt/sources.list.d/atom.list")
        }

    def check_apm_candiate(self, package: str) -> bool:
        """
        Ensure that an Atom plugin can be installed
        """

        if not(isinstance(package, str)):
            raise ValueError(f'expecting `str`, received {type(package)}')

        if not(
            (bash := shutil.which("bash")) and
                (apm := shutil.which("apm"))):
            raise ValueError
        try:
            self.executor.run(
                f'{apm} view {package}',
                self.executor.whoami)
        except Exception as e:
            return False
        return True

    def install_ppa(self):
        """
        GOAL: install the Atom PPA
        """

        gpg_url = self.link_dictionary["ATOM_GPG_URL"].link
        atom_list = self.file_footprint["ATOM_SOURCE"]

        gpg_dest = pathlib.Path("/tmp/gpgkey")
        content = requests.get(gpg_url).content

        with open(atom_list, "w") as fp:
            fp.write(
                "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main")

        with open(gpg_dest, "wb") as fp:
            fp.write(content)

        self.executor.run(
            f'sudo apt-key add {gpg_dest.resolve()}',
            self.executor.whoami)

    def add(self, plugins=['dbg-gdb', 'dbg', 'output-panel'], write=True):
        """
        GOAL: Get and install Atom with predefined plugins
        API usage: supply custom plugins list
        """

        if not(isinstance(plugins, list)):
            raise ValueError(f'expecting list, received {type(plugins)}')

        atom_conf_dir = pathlib.Path(f'/home/{self.executor.whoami}/.atom')

        self.install_ppa()

        # self.edit_deb_packages(self.packages, is_installing=True)

        for plugin in plugins:
            print(f'[INFO] Installing {plugin}...')
            self.executor.run(
                f'/usr/bin/apm install {plugin}',
                self.executor.whoami)
            self.executor.run(
                f'chown {self.executor.whoami} -R {atom_conf_dir}',
                self.executor.whoami)
        print("[INFO] Finished installing Atom")

        if(write):
            self.update_state(self.packages, True)

    def remove(self, write=False):
        # self.edit_deb_packages(self.packages, is_installing=False)
        self.file_footprint["ATOM_SOURCE"].unlink()
        if(write):
            self.update_state(self.packages, False)


class EmacsKeyword(EditorBaseKeyword):
    """
    Install or remove the Emacs editor
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'emacs', 'an adequite editor')
        self.packages: list[str] = ['emacs']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)


class EclipseKeyword(AbstractKeyword):
    """
    Attempts to grab a tar ball of the Eclipse installer
    and convert it into a Debian installer
    `eclipsetuffix` is the package name, so there is no conflict if Oracle
    rolls out an official way to install Eclipse
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'eclipse', 'a Java IDE')
        self.packages: list[str] = ['eclipsetuffix', 'openjdk-11-jdk']
        self.checkable_packages: list[str] = self.packages[0:]

        self.link_dictionary = {
            "ECLIPSE_URL": LinkPacket(
                link="http://mirror.umd.edu/eclipse/technology/epp/downloads/release/2020-06/R/eclipse-java-2020-06-R-linux-gtk-x86_64.tar.gz",
                is_git=False)}
        self.file_footprint = {"ECLIPSE_LAUNCHER": pathlib.Path(
            '/usr/share/applications/eclipse.desktop')}

    def add(self):
        """
        Install the Eclipse launcher
        If any issues arise post installation, please let the developers know ASAP
        """

        self.edit_deb_packages(self.packages[1:], is_installing=True)
        url = self.link_dictionary["ECLIPSE_URL"].link

        content = requests.get(url).content
        path = pathlib.Path("/tmp/installer.tar.gz")

        with open(path, "wb") as fp:
            fp.write(content)

        _DebTheBuilder = DebBuilder("eclipse", path)

        control = pathlib.Path("/tmp/control")

        with open(control, "w") as fp:
            contents = """
            Package: eclipsetuffix
            Version: 1.2021-06
            Section: editors
            Priority: optional
            Architecture: amd64
            Maintainer: Oracle
            Description: Java IDE created by Oracle
            Depends: openjdk-11-jdk
            """
            fp.write(textwrap.dedent(contents).strip())

        # scripts
        postrm = pathlib.Path("/tmp/postrm")
        postinst = pathlib.Path("/tmp/postinst")

        with open(postrm, "w") as fp:
            fp.writelines(
                ["#!/usr/bin/env bash", "sudo rm -i /usr/bin/eclipse"])

        with open(postinst, "w") as fp:
            fp.writelines(["#!/usr/bin/env bash",
                           "sudo ln -s /usr/eclipse/eclipse /usr/bin/eclipse"])
        _DebTheBuilder.make(control=control, scripts=[postinst, postrm])

        apt.debfile.DebPackage(filename="eclipsetuffix.deb").install()

        launcher = """
        [Desktop Entry]
        Encoding=UTF-8
        Name=Eclipse IDE
        Comment=Eclipse IDE
        Exec=/usr/bin/eclipse
        Icon=/usr/eclipse/icon.xpm
        Terminal=false
        Type=Application
        StartupNotify=false
        """

        launcher_path = self.file_footprint["ECLIPSE_LAUNCHER"]
        with open(launcher_path, "w") as fp:
            fp.write(launcher)

        self.update_state(self.packages, True)

    def remove(self):
        self.file_footprint["ECLIPSE_LAUNCHER"].unlink()
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)


class GeanyKeyword(EditorBaseKeyword):

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'geany', 'a lightweight GTK IDE')
        self.packages: list[str] = ['geany']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)


class NetbeansKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'netbeans', 'a Java IDE')
        self.packages: list[str] = ['netbeans']

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)


class VimKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'vim', 'an exquisite editor')
        self.packages: list[str] = ['vim', 'vim-gtk3']

    def add(self, vimrc_path=""):
        """
        Goal: install vim and added feature for vimrc (personal touch)
        """

        if not(isinstance(vimrc_path, str)):
            raise ValueError(
                f'expected `str`, obtained {type(vimrc_path).__name__}')

        if(vimrc_path):
            vrc = pathlib.Path(f'/home/{self.executor.whoami}/.vimrc')
            content = requests.get(vimrc_path).content
            with open(vrc, "wb") as fp:
                fp.write(content)
        self.edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages[:1], True)
        if(vimrc_path):
            self.executor.run(f'vim +silent +PluginInstall +qall')

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages[:1], False)


class VscodeKeyword(EditorBaseKeyword):
    """
    Not using the `apt` module, please be warned
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'code', 'Microsoft\'s text editor')
        self.packages: list[str] = ['code']
        self.checkable_packages = []
        self.link_dictionary = {
            "VSCODE_DEB": LinkPacket(
                link="https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64",
                is_git=False)}

    def add(self):
        url = self.link_dictionary["VSCODE_DEB"].link
        deb_path = "/tmp/vscode.deb"
        print("[INFO] Downloading installer...")
        # content = requests.get(url).content
        # with open(deb_path, "wb") as fp:
            # fp.write(content)
        apt.debfile.DebPackage(filename=deb_path).install()
        self.update_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)


class EditorKeywordContainer():
    def __init__(self, build_config=DEFAULT_BUILD_CONFIG):
        if not(isinstance(build_config, BuildConfig)):
            raise ValueError

        self.container: list[EditorBaseKeyword] = [
            AtomKeyword(build_config),
            # EclipseKeyword(build_config), NOTE : needs to undergo more
            # testing
            EmacsKeyword(build_config),
            GeanyKeyword(build_config),
            NetbeansKeyword(build_config),
            VimKeyword(build_config),
            VscodeKeyword(build_config)
        ]

    def obtain(self, value: str) -> tuple:
        if(not isinstance(value, str)):
            raise ValueError(f'incorrect type: {type(value)}')

        for keyword in self.container:
            if(keyword.name == value):
                return (True, keyword)
        return (False, None)
