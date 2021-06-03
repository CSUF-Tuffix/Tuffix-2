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
from Tuffix.Exceptions import *

class Editors():
    def __init__(self):
        # self.supported = [
            # 'atom',
            # 'emacs',
            # 'vim',
            # 'vscode'
        # ]

        self.supported = {
            "atom": self.atom,
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


    def atom(self):
        """
        GOAL: Get and install Atom with predefined plugins
        """

        packages = ['atom']

        atom_plugins = ['dbg-gdb',
                        'dbg',
                        'output-panel']

        self.executor.run(
            'sudo add-apt-repository -y ppa:webupd8team/atom',
            self.normal_user)
        atom_conf_dir = pathlib.Path(f'/home/{self.normal_user}/.atom')
        edit_deb_packages(packages, is_installing=True)

        for plugin in atom_plugins:
            print(f'[INFO] Installing {plugin}...')
            executor.run(f'/usr/bin/apm install {plugin}', self.normal_user)
            executor.run(
                f'chown {normal_user} -R {atom_conf_dir}',
                self.normal_user)
        print("[INFO] Finished installing Atom")

    def emacs(self):
        packages = ['emacs']
        self.executor.run(
            'sudo add-apt-repository -y ppa:kelleyk/emacs',
            normal_user)

        edit_deb_packages(packages, is_installing=True)

    def vim(self):
        packages = ['vim']
        edit_deb_packages(packages, is_installing=True)

    def vscode(self):
        packages = ['code']  # please check the name of VSCode

        asc_link = "https://packages.microsoft.com/keys/microsoft.asc"

        asc_path = pathlib.Path("/tmp/microsoft.asc")

        content = request.get(asc_link).content.decode("utf-8")

        with open(asc_path, "w") as f:
            f.write(content)

        subprocess.check_output(
            ('gpg', '--output', f'{gpg_path}', '--dearmor', f'{asc_path}'))

        vscode_ppa = "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

        self.executor.run(
            f'sudo add-apt-repository -y {vscode_ppa}',
            self.normal_user)

        edit_deb_packages(packages, is_installing=True)
