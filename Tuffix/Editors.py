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

from apt import debfile
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

    def rewrite_state(self, arguments: list, install=True):
        """
        Goal: update the state file
        """

        if not (isinstance(arguments, list) and isinstance(install, bool)):
            raise ValueError

        current_state = read_state(self.build_config)

        new_action = current_state.editors

        for argument in arguments:
            if not install:
                new_action.remove(argument)
            else:
                new_action.append(argument)

        new_state = State(
            self.build_config,
            self.build_config.version,
            current_state.installed,
            new_action,
        )
        new_state.write()


class BlankEditorKeyword(EditorBaseKeyword):
    # NOTE: please delete when done

    def __init__(self, build_config: BuildConfig):
        super().__init__(
            build_config,
            "blank",
            "this is a test editor keyword and should be discarded when done",
        )
        self.packages = ["cowsay"]
        self.checkable_packages = self.packages

    def add(self):
        self.rewrite_state([self.name], True)

    def remove(self):
        self.rewrite_state([self.name], False)


class AtomKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "atom", "Github's own editor")
        self.packages: list[str] = ["atom"]
        self.checkable_packages = []
        self.repo_payload = (
            "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main"
        )

        self.link_dictionary = {
            "ATOM_GPG_URL": LinkPacket(
                link="https://packagecloud.io/AtomEditor/atom/gpgkey", is_git=False
            )
        }

    def check_apm_candiate(self, package: str) -> bool:
        """
        Ensure that an Atom plugin can be installed
        """

        if not (isinstance(package, str)):
            raise ValueError(f"expecting `str`, received {type(package)}")

        if not ((bash := shutil.which("bash")) and (apm := shutil.which("apm"))):
            raise ValueError
        try:
            self.executor.run(f"{apm} view {package}", self.executor.whoami)
        except Exception as e:
            return False
        return True

    def install_ppa(self):
        """
        GOAL: install the Atom PPA
        """

        gpg_url = self.link_dictionary["ATOM_GPG_URL"].link

        gpg_dest = pathlib.Path("/tmp/gpgkey")
        content = requests.get(gpg_url).content

        with open(gpg_dest, "wb") as fp:
            fp.write(content)

        self.executor.run(
            f"sudo apt-key add {gpg_dest.resolve()}", self.executor.whoami
        )

        self.write_to_sources(self.repo_payload, True)

    def install_plugins(self, plugins: list = ["dbg-gdb", "dbg", "output-panel"]):
        """
        Install pre-approved Atom packages
        API usage: supply custom plugins list
        """

        if not (
            isinstance(plugins, list) and all([isinstance(_, str) for _ in plugins])
        ):
            raise ValueError

        atom_conf_dir = pathlib.Path(f"/home/{self.executor.whoami}/.atom")

        for plugin in plugins:
            print(f"[INFO] Installing {plugin}...")
            self.executor.run(f"/usr/bin/apm install {plugin}", self.executor.whoami)
            self.executor.run(
                f"chown {self.executor.whoami} -R {atom_conf_dir}", self.executor.whoami
            )

    def add(self, write=True, can_install_ppa=True):
        """
        GOAL: Get and install Atom with predefined plugins
        """

        if can_install_ppa:
            self.install_ppa()

        self.edit_deb_packages(self.packages, is_installing=True)

        self.install_plugins()

        print("[INFO] Finished installing Atom")

        if write:
            self.rewrite_state(self.packages, True)

    def remove(self, write=True):
        self.edit_deb_packages(self.packages, is_installing=False)

        if write:
            self.rewrite_state(self.packages, False)


class EmacsKeyword(EditorBaseKeyword):
    """
    Install or remove the Emacs editor
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "emacs", "an adequite editor")
        self.packages: list[str] = ["emacs"]

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.rewrite_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.rewrite_state(self.packages, False)


class GeanyKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "geany", "a lightweight GTK IDE")
        self.packages: list[str] = ["geany"]

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.rewrite_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.rewrite_state(self.packages, False)


class NetbeansKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "netbeans", "a Java IDE")
        self.packages: list[str] = ["netbeans"]

    def add(self):
        self.edit_deb_packages(self.packages, is_installing=True)
        self.rewrite_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.rewrite_state(self.packages, False)


class VimKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "vim", "an exquisite editor")
        self.packages: list[str] = ["vim", "vim-gtk3"]

    def add(self, vimrc_path=""):
        """
        Goal: install vim and added feature for vimrc (personal touch)
        """

        if not (isinstance(vimrc_path, str)):
            raise ValueError(f"expected `str`, obtained {type(vimrc_path).__name__}")

        if vimrc_path:
            vrc = pathlib.Path(f"/home/{self.executor.whoami}/.vimrc")
            content = requests.get(vimrc_path).content
            with open(vrc, "wb") as fp:
                fp.write(content)
        self.edit_deb_packages(self.packages, is_installing=True)
        self.rewrite_state(self.packages[:1], True)
        if vimrc_path:
            self.executor.run(f"vim +silent +PluginInstall +qall")

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.rewrite_state(self.packages[:1], False)


class VscodeKeyword(EditorBaseKeyword):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, "code", "Microsoft's text editor")
        self.packages: list[str] = [
            "gnupg",
            "libgbm1",
            "libgtk-3-0",
            "libnss3",
            "libsecret-1-0",
            "libxkbfile1",
            "libxss1",
            "code",
        ]
        self.checkable_packages = self.packages[:-1]
        self.link_dictionary = {
            "VSCODE_GPG": LinkPacket(
                link="https://packages.microsoft.com/keys/microsoft.asc", is_git=False
            )
        }
        self.repo_payload = (
            "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
        )

    def install_ppa(self):
        """
        GOAL: install the PPA
        """

        gpg_url = self.link_dictionary["VSCODE_GPG"].link

        gpg_dest = pathlib.Path("/tmp/gpgkey")
        content = requests.get(gpg_url).content

        with open(gpg_dest, "wb") as fp:
            fp.write(content)

        self.executor.run(
            f"sudo apt-key add {gpg_dest.resolve()}", self.executor.whoami
        )

        self.write_to_sources(self.repo_payload, True)

    def add(self, can_install_ppa: bool = True):
        if can_install_ppa:
            self.install_ppa()

        self.edit_deb_packages(self.packages, is_installing=True)

        print("[INFO] Finished installing vscode")

        self.rewrite_state(self.packages, True)

    def remove(self):
        self.edit_deb_packages(self.packages, is_installing=False)
        self.rewrite_state(self.packages, False)


class EditorKeywordContainer:
    def __init__(self, build_config=DEFAULT_BUILD_CONFIG):
        if not (isinstance(build_config, BuildConfig)):
            raise ValueError

        self.container: list[EditorBaseKeyword] = [
            AtomKeyword(build_config),
            BlankEditorKeyword(build_config),
            EmacsKeyword(build_config),
            GeanyKeyword(build_config),
            NetbeansKeyword(build_config),
            VimKeyword(build_config),
            VscodeKeyword(build_config),
        ]

    def obtain(self, value: str) -> tuple:
        if not isinstance(value, str):
            raise ValueError(f"incorrect type: {type(value)}")

        for keyword in self.container:
            if keyword.name == value:
                return (True, keyword)
        return (False, None)
