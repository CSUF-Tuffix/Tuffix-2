##########################################################################
# editors
# AUTHOR: Jared Dyreson
##########################################################################


"""
Supported:
- atom
- emacs
- vi(m)
- vscode
"""
from Tuffix.SudoRun import SudoRun
from Tuffix.KeywordHelperFunctions import *
from Tuffix.Exceptions import *

import apt
import os
import pathlib
import requests
import subprocess
import tarfile

class Editors():
    def __init__(self):

        self.supported = {
            "atom": self.atom,
            "eclipse": self.eclipse,
            "emacs": self.emacs,
            "vim": self.vim,
            "vscode": self.vscode
        }

        self.executor = SudoRun()
        self.normal_user = self.executor.whoami

    def prompt(self, require_input=(None, None)):
        """
        require_input: tuple
        Goal: select correct editor to install and return proper function pointer
        """

        status, response = require_input

        if not(status):
            string = '\n'.join(f'  {[x]} {editor}' for x, editor, _ in enumerate(self.supported.items()))
            response = len(self.supported) + 1

            while(response > len(self.supported)):
                response = int(input(f'[INFO] Select editor:\n{string}\n: '))
        try:
            word = list(self.supported.keys())[response]
        except IndexError:
            raise UsageError(f'[ERROR] Unsupported index of {response}')
        print(f'[INFO] You have selected: {response} -> {word}')
        assert(callable(self.supported[word])) # ensure the function pointer is valid
        return self.supported[word] # return function pointer to installer


    def atom(self, plugins = ['dbg-gdb', 'dbg', 'output-panel']):
        """
        GOAL: Get and install Atom with predefined plugins
        API usage: supply custom plugins list
        """

        packages = ['atom']

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

        edit_deb_packages(packages, is_installing=True)


        for plugin in plugins:
            print(f'[INFO] Installing {plugin}...')
            self.executor.run(f'/usr/bin/apm install {plugin}', self.normal_user)
            self.executor.run(
                f'chown {self.normal_user} -R {atom_conf_dir}',
                self.normal_user)
        print("[INFO] Finished installing Atom")

    def emacs(self):
        packages = ['emacs']
        self.executor.run(
            'sudo add-apt-repository -y ppa:kelleyk/emacs',
            self.normal_user)

        edit_deb_packages(packages, is_installing=True)

    def vim(self, vimrc_path=""):
        """
        Goal: install vim and added feature for vimrc (personal touch)
        """

        if(vimrc_path):
            vrc = pathlib.Path(f'/home/{self.normal_user}/.vimrc')
            content = requests.get(vimrc_path).content
            with open(vrc, "wb") as fp:
                fp.write(content)
        packages = ['vim']
        edit_deb_packages(packages, is_installing=True)

    def vscode(self):
        """
        Not using the `apt` module, please be warned
        """        

        url = "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
        deb_path = "/tmp/vscode.deb"
        print("[INFO] Downloading installer...")
        content = requests.get(url).content
        with open(deb_path, "wb") as fp:
            fp.write(content)
        apt.debfile.DebPackage(filename=deb_path).install()

    def eclipse(self):
        """
        Not using the `apt` module, please be warned
        Source: https://www.itzgeek.com/post/how-to-install-eclipse-ide-on-ubuntu-20-04/
        """

        packages = ['openjdk-11-jdk']
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


