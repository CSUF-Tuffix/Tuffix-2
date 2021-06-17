##########################################################################
# user-facing commands (init, add, etc.)
# AUTHORS: Kevin Wortman, Jared Dyreson
##########################################################################

from Tuffix.Configuration import BuildConfig, State, DEFAULT_BUILD_CONFIG
from Tuffix.KeywordHelperFunctions import DEFAULT_PICKLER
from Tuffix.Constants import *
from Tuffix.Exceptions import *
from Tuffix.Keywords import *
from Tuffix.Status import status
from Tuffix.UtilityFunctions import *
from Tuffix.Editors import EditorKeywordContainer
from Tuffix.SudoRun import SudoRun

import os
import json
import pickle  # dump custom class instance to disk
from termcolor import colored
# so we can pass in function pointers with predefined args
from functools import partial
import shutil


class AbstractCommand:
    """
    abstract base class for one of the user-visible tuffix commands, e.g.
    init, status, etc

    build_config: a BuildConfig object
    name: the string used for the command one the commandline, e.g 'init'.
    Must be a non-empty string of lower-case letters.
    description: description of the command printed in usage help. Must be
    a nonempty string.
    """

    def __init__(self, build_config, name, description):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(name, str) and
                len(name) > 0 and
                name.isalpha() and
                name.islower() and
                isinstance(description, str)):
            raise ValueError
        self.build_config = build_config
        self.name = name
        self.description = description

    def __repr__(self):
        return f"""
        Class: {self.__name__}
        Name: {self.name}
        Description: {self.description}
        """

    def execute(self, arguments):
        """
        Execute the command.
        arguments: list of commandline arguments after the command name.
        A concrete implementation should:
        Execute the command, then return and int for the exit code that tuffix
        should return to the OS.
        Raise UsageError if arguments are invalid commandline arguments.
        Raise another kind of MessageException in any other error case.
        execute may only throw MessageException subtypes (including UsageError);
        other exceptions should be caught and rethrown as a MessageException.
        """

        raise NotImplementedError


class MarkCommand(AbstractCommand):
    """
    GOAL: combine both the add and remove keywords
    This prevents us for not writing the same code twice.
    They are essentially the same function but they just call a different method

    NOT AVAILABLE TO PUBLIC USE (therefore not meant to be added to list of viable commands)
    """

    def __init__(self, build_config, command):
        super().__init__(build_config, 'mark', 'mark (install/remove) one or more keywords')
        if not(isinstance(command, str)):
            raise ValueError

        # either select the add or remove from the Keywords
        self.command = command
        self.container = KeywordContainer(build_config)

    def search(self, pattern: str) -> tuple:
        if(not isinstance(pattern, str)):
            raise ValueError

        _re = re.compile(f'{pattern}.json', flags=re.IGNORECASE)
        # TODO : change this path to something in DEFAULT_BUILD_CONFIG
        for dirpath, _, filepath in os.walk('json_payload/'):
            for _file in filepath:
                match = _re.match(_file)
                if(match):
                    # If the JSON file is found, we need to now dynamically create a class
                    NewClass = DEFAULT_CLASS_GENERATOR.generate(
                        f'{dirpath}/{_file}')
                    NewClassInstance = NewClass()
                return (True, NewClassInstance)
        return (False, None)

    def rewrite_state(self, current_state, keyword, install):
        """
        Goal: update the state file
        """
        # TODO : check what type keyword is

        # if not(isinstance(current_state, Keyword.State) and
        # isinstance(keyword, Keyword) and
        # isinstance(install, bool)):
        # raise ValueError

        current_state = read_state(self.build_config)
        new_action = current_state.installed

        if(not install):
            new_action.remove(keyword.name)
        else:
            new_action.append(keyword.name)

        new_state = State(self.build_config,
                          self.build_config.version,
                          new_action,
                          current_state.editors)
        new_state.write()

    def run_commands(self, container: list, install: bool):
        """
        Goal: execute a series of keywords given in a list container
        """

        if not(isinstance(container, list) and
               isinstance(install, bool)):
            raise ValueError

        current_state = read_state(self.build_config)

        verb, past = (
            "installing", "installed") if install else (
            "removing", "removed")

        for status, command in container:
            if((command.name in current_state.installed)):
                if(install):
                    raise UsageError(
                        f'[WARNING] Tuffix: cannot add {command.name}, it is already installed')
            elif((command.name not in current_state.installed) and (not install)):
                raise UsageError(
                    f'[ERROR]: Tuffix: Cannot remove candidate {command.name}; not installed')

            print(f'[INFO] Tuffix: {verb} {command.name}')

            try:
                getattr(command, self.command)()
            except AttributeError:
                raise UsageError(
                    f'[INTERNAL ERROR] {command.__name__} does not have the function {self.command}')

            self.rewrite_state(None, command, install)

            print(f'[INFO] Tuffix: successfully {past} {command.name}')

    def execute(self, arguments: list, custom=(None, None)):
        """
        Goal: install or remove keywords
        """
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError

        if not(arguments):
            raise UsageError(
                "[ERROR] You must supply at least one keyword to mark")

        # This pertains to custom keywords we have defined in a JSON file
        custom_status, custom_command = custom

        if(custom_status):
            # Emplace this into the list of possible keywords
            collection = [(True, custom_command)]
        else:
            # ./tuffix add base media latex
            collection = [self.container.obtain(x) for x in arguments]

        for x, element in enumerate(collection):
            # if the command could not be found and we need to remove it
            status, command = element
            if(not status and not command):
                # search the pickle jar to load the custom class
                status, obj = self.search(arguments[x])
                if(not status):
                    raise ValueError(
                        f'[INTERNAL ERROR] Tuffix: Could not find custom class for {arguments[x]}')
                collection[x] = obj

        install = True if self.command == "add" else False

        # ./tuffix add all
        # ./tuffix remove all

        if(arguments[0] == "all"):
            try:
                input(
                    "[INFO] Tuffix: Are you sure you want to install/remove all packages? Press enter to continue or CTRL-D to exit: ")
            except EOFError:
                quit()
            if(install):
                collection = self.container.container  # all keywords
            else:
                collection = [self.container.obtain(
                    x) for x in state.installed]  # all installed

        ensure_root_access()
        self.run_commands(collection, install)
        os.system("apt autoremove")  # purge system of unneeded dependencies


class AddCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'add', 'add (install) one or more keywords')
        self.mark = MarkCommand(build_config, self.name)

    def execute(self, arguments):
        self.mark.execute(arguments)


class CustomCommand(AbstractCommand):

    def __init__(self, build_config):
        super().__init__(build_config, 'custom', 'user-defined json payload')

    def execute(self, arguments: list):
        for path in arguments:
            if(not os.path.exists(path)):
                raise FileNotFoundError(f'[ERROR] Could not load {path}')

            NewClass = DEFAULT_CLASS_GENERATOR.generate(path)

            path = pathlib.Path(path)

            NewClassInstance = NewClass()

            self.mark = MarkCommand(DEFAULT_BUILD_CONFIG, "add")
            self.mark.execute([NewClassInstance.name],
                              (True, NewClassInstance))

            shutil.copyfile(path, DEFAULT_BUILD_CONFIG.json_state_path / path.stem)


class DescribeCommand(AbstractCommand):

    def __init__(self, build_config):
        super().__init__(build_config, 'describe', 'describe a given keyword')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError
        if(len(arguments) != 1):
            raise UsageError("Please supply at only one keyword to describe")
        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        status, keyword = k_container.obtain(arguments[0])

        print(f'{keyword.name}: {keyword.description}')


class EditorCommand(AbstractCommand):

    def __init__(self, build_config):
        super().__init__(build_config, 'editor', 'install a given editor; ')
        self.editors = EditorKeywordContainer()

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError
        if not(arguments):
            raise UsageError("Please supply at least one editor to install")

        current_state = read_state(self.build_config)
        install = (arguments[0] == "add")

        for editor in arguments[1:]:
            # run each editor command, will raise KeyError if command name is not found
            # make it lowercase for sanity
            status, command = self.editors.obtain(editor)
            if not(status):
                raise UsageError(f'editor: {editor} is not supported')

            if((command.name in current_state.installed)):
                if(install):
                    raise UsageError(
                        f'[WARNING] Tuffix: cannot add {command.name}, it is already installed')
            if(install):
                command.add()
            else:
                command.remove()
        command.update_state(arguments[1:], install)
        # self.update_state(current_state, arguments[1:], install)


class RekeyCommand(AbstractCommand):
    """
    What is this?
    """

    whoami = os.getlogin()
    # name, email, passphrase = input("Name: "), input("Email: "), getpass.getpass("Passphrase: ")

    def __init__(self, build_config):
        super().__init__(build_config, 'rekey', 'regenerate ssh and/or gpg key')

    def ssh_gen(self):
        ssh_dir = pathlib.Path(f'/home/{self.whoami}/.ssh')
        key = RSA.generate(4096)
        private_path = pathlib.Path(os.path.join(ssh_dir, 'id_rsa'))
        with open(private_path, "wb") as fp:
            fp.write(key.exportKey('PEM'))

        public_key = key.publickey()
        public_path = pathlib.Path(os.path.join(ssh_dir, 'id_rsa.pub'))
        with open(public_path, "wb") as fp:
            fp.write(public_key.exportKey('OpenSSH'))
        os.chmod(public_path, 0o600)
        os.chmod(private_path, 0o600)
        print(f'sending keys to {self.build_config.server_path}')
        subprocess.call(
            f'ssh-copy-id -i {public_path} {self.build_config.server_path}'.split())

    def gpg_gen(self):

        gpg = gnupg.GPG(gnupghome=f'/home/{self.whoami}/.gnupg')
        gpg.encoding = 'utf-8'
        gpg_file = pathlib.Path(os.path.join(gpg.gnupghome, 'tuffix_key.asc'))

        print("[INFO] Please wait a moment, this may take some time")
        input_data = gpg.gen_key_input(
            key_type="RSA",
            key_length=4096,
            name_real=self.name,
            name_comment=f'Autogenerated by tuffix for {self.name}',
            name_email=self.email,
            passphrase=self.passphrase
        )
        key = gpg.gen_key(input_data)
        public = gpg.export_keys(key.fingerprint, False)
        private = gpg.export_keys(
            key.fingerprint,
            False,
            passphrase=self.passphrase
        )

        with open(gpg_file, 'w') as fp:
            fp.write(public)
            fp.write(private)
        print(f'sending the keys to {self.build_config.server_path}')
        os.system("ssh-add")

        # not sure how this entirely works.....
        # gpg.send_keys(f'{self.build_config.server_path}', key.fingerprint)

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError
        if(len(arguments) != 1):
            raise UsageError("Please supply at only one keyword to regen")

        regen_entity = arguments[0]

        if((regen_entity == "ssh")):
            self.ssh_gen()

        elif((regen_entity == "gpg")):
            self.gpg_gen()

        else:
            raise UsageError(
                f'[ERROR] Invalid selection {regen_entity}. "ssh" and "gpg" are the only valid selectors')


class InitCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'init', 'initialize tuffix')

    def configure_git(self, username=None, mail=None):
        """
        GOAL: Configure git
        """

        keeper = SudoRun()
        whoami = keeper.whoami

        username = input("Git username: ")
        mail = input("Git email: ")
        git_conf_file = pathlib.Path(f'/home/{whoami}/.gitconfig')
        commands = [
            f'git config --file {git_conf_file} user.name {username}',
            f'git config --file {git_conf_file} user.email {mail}'
        ]
        for command in commands:
            keeper.run(command, whoami)
        print(colored("Successfully configured git", 'green'))

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError

        if len(arguments) != 0:
            raise UsageError("init command does not accept arguments")
        if(STATE_PATH.exists()):
            raise UsageError("init has already been done")

        # ensure we have our PPA installed

        gpg_url = "https://www.tuffix.xyz/repo/KEY.gpg"
        tuffix_list = pathlib.Path("/etc/apt/sources.list.d/tuffix.list")

        gpg_dest = pathlib.Path("/tmp/tuffix.gpg")
        executor = SudoRun()

        content = requests.get(gpg_url).content
        with open(gpg_dest, "wb") as fp:
            fp.write(content)
        with open(tuffix_list, "w") as fp:
            fp.write("deb https://www.tuffix.xyz/repo focal main")

        executor.run(
            f'sudo apt-key add {gpg_dest.resolve()}',
            executor.whoami)

        create_state_directory(self.build_config)

        state = State(self.build_config, self.build_config.version, [], [])
        state.write()

        print('[INFO] Tuffix init succeeded')


class InstalledCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'installed', 'list all currently-installed keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError

        if len(arguments) != 0:
            raise UsageError("installed command does not accept arguments")

        state = read_state(self.build_config)

        if len(state.installed) == 0:
            print('[INFO] No keywords are installed')
        else:
            print('[INFO] Tuffix installed keywords:')
            for name in state.installed:
                print(name)


class ListCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'list', 'list all available keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError

        if len(arguments) != 0:
            raise UsageError("list command does not accept arguments")

        print('tuffix list of keywords:')
        container = KeywordContainer(self.build_config)
        for keyword in container.container:
            print(f'{keyword.name.ljust(KEYWORD_MAX_LENGTH)}   {keyword.description}')


class StatusCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'status', 'status of the current host')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
            raise ValueError

        if len(arguments) != 0:
            raise UsageError("status command does not accept arguments")

        for line in status():
            print(line)


class SystemUpgradeCommand(AbstractCommand):
    packages = []

    def __init__(self, build_config):
        super().__init__(build_config,
                         'supgrade',
                         'Upgrade the entire system')

    def execute(self, arguments):
        # source :
        # https://stackoverflow.com/questions/3092613/python-apt-get-list-upgrades
        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.upgrade()
        for pkg in cache.get_changes():  # changed from getChanges
            try:
                if(pkg.is_upgradable):
                    print(f'[INFO] Upgrading {pkg.name}....')
                    pkg.mark_install()
                    cache.commit()
            except Exception as error:
                raise EnvironmentError(
                    f'[ERROR] Could not install {pkg.shortname}. Got error of {error}')


class RemoveCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'remove', 'remove (uninstall) one or more keywords')
        self.mark = MarkCommand(build_config, self.name)

    def execute(self, arguments):
        self.mark.execute(arguments)


class BackgroundCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'background', 'set a background')

    def execute(self, arguments):
        try:
            ensure_root_access()
        except UsageError:
            pass
        else:
            raise UsageError(
                '[ERROR] This command cannot be run as root, cowardly refusing')

        """
        There should be some really cool match case stuff here but keep it simple stupid
        """

        if((_len := len(arguments)) < 1):
            print(arguments)
            raise UsageError(
                f'insufficient arguments, expected 1, received {_len}')
        path = arguments[0]
        if(path == "user-submitted"):
            print("retrieve from some nice function call")
            return
        else:
            path = pathlib.Path(path)
            if not(path.exists()):
                raise FileNotFoundError(
                    f'[ERROR] File {path.resolve()} does not exist')
        set_background(path)


def all_commands(build_config):
    """
    CURRENT COMMANDS SUPPORTED
    Create and return a list containing one instance of every known
    AbstractCommand, using build_config and state for each.
    """

    if not isinstance(build_config, BuildConfig):
        raise ValueError
    # alphabetical order
    return [AddCommand(build_config),
            BackgroundCommand(build_config),
            CustomCommand(build_config),
            DescribeCommand(build_config),
            InitCommand(build_config),
            InstalledCommand(build_config),
            ListCommand(build_config),
            StatusCommand(build_config),
            RemoveCommand(build_config),
            SystemUpgradeCommand(build_config),
            EditorCommand(build_config)
            ]
    # RekeyCommand(build_config)]
