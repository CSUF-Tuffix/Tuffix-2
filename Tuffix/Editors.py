##########################################################################
# editors
# AUTHOR: Jared Dyreson
##########################################################################


"""
Supported:
- atom
- eclipse
- emacs
- geany
- netbeans
- vi(m)
- vscode
"""

# NOTE : bug present in class structure where packages variable is not defined
# must use the self.name attr to get the package name. Unknown cause

from Tuffix.Keywords import AbstractKeyword

from Tuffix.SudoRun import SudoRun
from Tuffix.KeywordHelperFunctions import *
from Tuffix.Exceptions import *
from Tuffix.Configuration import *

import apt
import os
import pathlib
import requests
import subprocess
import tarfile

class EditorBaseKeyword(AbstractKeyword):
    def __init__(self, build_config: BuildConfig, name: str, description: str):
        super().__init__(build_config, name, description)
        self.build_config = build_config

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

    def add(self, plugins = ['dbg-gdb', 'dbg', 'output-panel']):
        """
        GOAL: Get and install Atom with predefined plugins
        API usage: supply custom plugins list
        """

        if not(isinstance(plugins, list)):
            raise ValueError(f'expecting list, received {type(plugins)}')


        atom_conf_dir = pathlib.Path(f'/home/{self.normal_user}/.atom')

        gpg_url = "https://packagecloud.io/AtomEditor/atom/gpgkey"
        atom_list = pathlib.Path("/etc/apt/sources.list.d/atom.list")

        gpg_dest = pathlib.Path("/tmp/gpgkey")
        content = requests.get(gpg_url).content


        with open(atom_list, "w") as fp:
            fp.write("deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main")

        with open(gpg_dest, "wb") as fp:
            fp.write(content)

        self.executor.run(
            f'sudo apt-key add {gpg_dest.resolve()}',
            self.normal_user)

        edit_deb_packages(self.packages, is_installing=True)


        for plugin in plugins:
            print(f'[INFO] Installing {plugin}...')
            self.executor.run(f'/usr/bin/apm install {plugin}', self.normal_user)
            self.executor.run(
                f'chown {self.normal_user} -R {atom_conf_dir}',
                self.normal_user)
        print("[INFO] Finished installing Atom")
        self.update_state(self.build_config, self.packages, True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        pathlib.Path("/etc/apt/sources.list.d/atom.list").unlink()
        self.update_state(self.build_config, self.packages, False)

class EmacsKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'emacs', 'an adequite editor')
        self.packages: list[str] = ['emacs']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class EclipseKeyword(AbstractKeyword):
    """
    Not using the `apt` module, please be warned
    Source: https://www.itzgeek.com/post/how-to-install-eclipse-ide-on-ubuntu-20-04/
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'eclipse', 'a Java IDE')
        self.packages: list[str] = ['openjdk-11-jdk']

    def add(self):
        edit_deb_packages(packages, is_installing=True)

        url = "http://mirror.umd.edu/eclipse/technology/epp/downloads/release/2020-06/R/eclipse-java-2020-06-R-linux-gtk-x86_64.tar.gz"

        content = requests.get(url).content
        path = pathlib.Path("/tmp/installer.tar.gz")

        with open(path, "wb") as fp:
            fp.write(content)

        tarfile.open(path).extractall('/usr')
        os.system("sudo ln -s /usr/eclipse/eclipse /usr/bin/eclipse")

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
        launcher_path = pathlib.Path('/usr/share/applications/eclipse.desktop')
        with open(launcher_path, "w") as fp:
            fp.write(launcher)

        self.update_state(self.packages, True)
    def remove(self):
        # TODO : find where uninstaller for this package is located
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class GeanyKeyword(EditorBaseKeyword):

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'geany', 'a lightweight GTK IDE')
        self.packages: list[str] = ['geany']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class NetbeansKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'netbeans', 'a Java IDE')
        self.packages: list[str] = ['netbeans']

    def add(self):
        edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages, True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class VimKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'vim', 'an exquisite editor')
        self.packages: list[str] = ['vim', 'vim-gtk3']

    def add(self, vimrc_path=""):
        """
        Goal: install vim and added feature for vimrc (personal touch)
        """

        if(vimrc_path):
            vrc = pathlib.Path(f'/home/{self.normal_user}/.vimrc')
            content = requests.get(vimrc_path).content
            with open(vrc, "wb") as fp:
                fp.write(content)
        # edit_deb_packages(self.packages, is_installing=True)
        self.update_state(self.packages[:1], True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class VscodeKeyword(EditorBaseKeyword):
    """
    Not using the `apt` module, please be warned
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'vscode', 'Microsoft\'s text editor')
        self.packages: list[str] = ['code']

    def add(self):
        url = "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
        deb_path = "/tmp/vscode.deb"
        print("[INFO] Downloading installer...")
        content = requests.get(url).content
        with open(deb_path, "wb") as fp:
            fp.write(content)
        apt.debfile.DebPackage(filename=deb_path).install()
        self.update_state(self.packages, True)

    def remove(self):
        edit_deb_packages(self.packages, is_installing=False)
        self.update_state(self.packages, False)

class EditorKeywordContainer():
    def __init__(self, build_config=DEFAULT_BUILD_CONFIG):
        if not(isinstance(build_config, BuildConfig)):
            raise ValueError

        self.container: list[EditorBaseKeyword] = [
            AtomKeyword(build_config),
            EclipseKeyword(build_config),
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
