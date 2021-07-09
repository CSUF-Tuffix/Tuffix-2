##########################################################################
# user-facing commands (init, add, etc.)
# AUTHORS: Kevin Wortman, Jared Dyreson
##########################################################################

from Tuffix.Configuration import BuildConfig, State, DEFAULT_BUILD_CONFIG
from Tuffix.Constants import *
from Tuffix.Exceptions import *
from Tuffix.Keywords import *
from Tuffix.Status import status, ensure_root_access
from Tuffix.Editors import AtomKeyword
from Tuffix.SudoRun import SudoRun
from Tuffix.AbstractKeyword import AbstractKeyword

import os
import json
import pickle  # dump custom class instance to disk
from termcolor import colored
# so we can pass in function pointers with predefined args
from functools import partial
import shutil
import apt
import inspect


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

    def __init__(self, build_config: BuildConfig, name: str, description: str):
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
        Name: {self.name}
        Description: {self.description}
        """

    def execute(self, arguments: list):
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


class AddRemoveHelper():
    """
    GOAL: combine both the add and remove keywords
    This prevents us for not writing the same code twice.
    They are essentially the same function but they just call a different method

    NOT AVAILABLE TO PUBLIC USE (therefore not meant to be added to list of viable commands)
    """

    def __init__(self, build_config: BuildConfig, command: str):
        if not(isinstance(command, str) and
               isinstance(build_config, BuildConfig)):
            raise ValueError

        # either select the add or remove from the Keywords
        self.build_config = build_config
        self.command = command
        self.container = KeywordContainer(build_config)

    def search(self, pattern: str) -> tuple:
        if(not isinstance(pattern, str)):
            raise ValueError

        _re = re.compile(f'{pattern}.json', flags=re.IGNORECASE)
        # NOTE: check if this works
        for dirpath, _, filepath in os.walk(self.build_config.json_state_path):
            for _file in filepath:
                if((match := _re.match(_file))):
                    # If the JSON file is found, we need to now dynamically
                    # create a class
                    path = pathlib.Path(f'{dirpath}/{_file}')
                    NewClass = DEFAULT_CLASS_GENERATOR.generate(
                        path.resolve(), self.build_config)
                    return (True, NewClass())
        return (False, None)

    def obtain_correct_attribute(self, keyword: AbstractKeyword, state: State):
        # same code in UnitTests/BaseEditorTest

        _type = type(keyword)
        if(issubclass(_type, AbstractKeyword) and
           not issubclass(_type, EditorBaseKeyword)):
            correct_attr = (True, False, "AbstractKeyword")
        else:
            correct_attr = (False, True, "EditorBaseKeyword")

        regular_keyword, editor, __name = correct_attr
        if(regular_keyword):
            return (__name, getattr(state, 'installed'))
        return (__name, getattr(state, 'editors'))

    def rewrite_state(self, keyword: AbstractKeyword, install: bool):
        """
        Goal: update the state file
        """
        if not(issubclass(keyword, AbstractKeyword) and
               isinstance(install, bool)):
            raise ValueError

        current_state = read_state(self.build_config)
        _type, attribute = self.obtain_correct_attribute(
            keyword, current_state)

        if(not install):
            new_action.remove(keyword.name)
        else:
            new_action.append(keyword.name)

        new_state = State(self.build_config,
                          self.build_config.version,
                          new_action if (
                              _type == "AbstractKeyword") else current_state.installed,
                          new_action if (_type == "EditorBaseKeyword") else current_state.editors)
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

            self.rewrite_state(command, install)

            print(f'[INFO] Tuffix: successfully {past} {command.name}')

    def execute(self, arguments: list, custom=(None, None), override=True):
        """
        Goal: install or remove keywords
        """

        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments]) and
                isinstance(override, bool)):
            raise ValueError

        if not(arguments):
            raise UsageError(
                "[ERROR] You must supply at least one keyword to mark")

        ensure_root_access()

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
            if not(override):
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

        self.run_commands(collection, install)
        os.system("apt autoremove -y")  # purge system of unneeded dependencies


class AddCommand(AbstractCommand):
    """
    Add a valid keyword either defined in Tuffix/Keywords.py or
    defined as a JSON file passed via the command line
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'add', 'add (install) one or more keywords')
        self.mark = AddRemoveHelper(build_config, self.name)

    def execute(self, arguments: list):
        if not(isinstance(arguments, list) and
               all([isinstance(_, str) for _ in arguments])):
            raise ValueError
        self.mark.execute(arguments)


class CustomCommand(AbstractCommand):
    """
    User defined keyword that gets generated via a JSON file
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'custom', 'user-defined json payload')

    def execute(self, arguments: list):
        if not(isinstance(arguments, list) and
               all([isinstance(_, str) for _ in arguments])):
            raise ValueError

        for path in arguments:
            path = pathlib.Path(path)

            if not(path.is_file()):
                raise FileNotFoundError(f'[ERROR] Could not load {path}')

            NewClass = DEFAULT_CLASS_GENERATOR.generate(
                path, self.build_config)

            NewClassInstance = NewClass()

            self.mark = AddRemoveHelper(self.build_config, "add")
            self.mark.execute([NewClassInstance.name],
                              (True, NewClassInstance))

            shutil.copyfile(
                path, self.build_config.json_state_path / path.stem)


class DescribeCommand(AbstractCommand):

    """
    Describe a valid keyword either defined in Tuffix/Keywords.py or as
    a JSON file
    """

    def __init__(self, build_config):
        super().__init__(build_config, 'describe', 'describe a given keyword')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(_, str) for _ in arguments])):
            raise ValueError(f'received type: {type(arguments[0])}')
        if(len(arguments) != 1):
            raise UsageError("Please supply at only one keyword to describe")
        k_container = KeywordContainer(DEFAULT_BUILD_CONFIG)
        status, keyword = k_container.obtain(arguments[0])

        print(f'{keyword.name}: {keyword.description}')


class InitCommand(AbstractCommand):
    """
    Initialize Tuffix by:
        - creating the directory structure
        - configure git
        - install the Tuffix PPA
        - install the Atom text editor

    Instructors should tell students to make an account on Github
    """

    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'init', 'initialize tuffix')

    def create_state_directory(self):
        """
        Create the directory for the state file, unless it already exists
        """

        ensure_root_access()
        os.makedirs(self.build_config.state_path.parent, exist_ok=True)

        new_state = State(self.build_config,
                          self.build_config.version,
                          [], [])
        new_state.write()

        os.makedirs(self.build_config.json_state_path,
                    exist_ok=True)  # for custom commands

    def remove_state_directory(self):
        """
        Remove the current state path
        """

        ensure_root_access()
        shutil.rmtree(self.build_config.state_path.parent)

    def configure_git(self, username=None, mail=None):
        """
        GOAL: Configure Git
        """

        keeper = SudoRun()
        whoami = keeper.whoami

        username = input("Git username: ") if not username else username
        mail = input("Git email: ") if not mail else mail
        git_conf_file = pathlib.Path(f'/home/{whoami}/.gitconfig')
        commands = [
            f'git config --file {git_conf_file} user.name {username}',
            f'git config --file {git_conf_file} user.email {mail}'
        ]
        for command in commands:
            keeper.run(command, whoami)
        print(colored("Successfully configured git", 'green'))

    def configure_ppa(self):
        """
        Goal: Install PPA
        """

        gpg_url = "https://www.tuffix.xyz/repo/KEY.gpg"
        tuffix_list = pathlib.Path("/etc/apt/sources.list.d/tuffix.list")

        gpg_dest = pathlib.Path("/tmp/tuffix.gpg")
        executor = SudoRun()

        content = requests.get(gpg_url).content
        with open(gpg_dest, "wb") as gd, open(tuffix_list, "w") as tl:
            gd.write(content)
            tl.write("deb https://www.tuffix.xyz/repo focal main")

        executor.run(
            f'sudo apt-key add {gpg_dest.resolve()}',
            executor.whoami)

    def install_atom(self, write=False):
        AtomKeyword(self.build_config).add(write=write)

    def execute(self, arguments: list):
        if not (isinstance(arguments, list) and
                all([isinstance(_, str) for _ in arguments]) and
                not arguments):
            # this should also be caught when testing (give multiple args)
            raise ValueError

        if(STATE_PATH.exists()):
            raise UsageError("init has already been done")

        self.create_state_directory()

        self.configure_ppa()
        self.configure_git()
        self.install_atom(write=True)

        state = State(self.build_config,
                      self.build_config.version, [], ["atom"])
        state.write()

        print('[INFO] Tuffix init succeeded')


class InstalledCommand(AbstractCommand):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'installed', 'list all currently-installed keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                not arguments):
            raise ValueError

        state = read_state(self.build_config)

        if((argc := len(state.installed)) == 0):
            print('[INFO] No keywords are installed')
        else:
            print(f'[INFO] Tuffix installed keywords ({argc}):')
            for name in state.installed:
                print(name)


class ListCommand(AbstractCommand):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'list', 'list all available keywords')

    def execute(self, arguments: list):
        if not(isinstance(arguments, list) and
                ((argc := len(arguments) >= 0))):
            raise ValueError

        container = KeywordContainer(self.build_config).container
        print('[INFO] Tuffix list of keywords:')
        for keyword in container:
            print(f'{keyword.name.ljust(KEYWORD_MAX_LENGTH)}   {keyword.description}')


class StatusCommand(AbstractCommand):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'status', 'status of the current host')

    def execute(self, arguments: list):
        if not(isinstance(arguments, list) and
                ((argc := len(arguments)) >= 0)):
            raise ValueError

        messsage = (None, None)
        try:
            for line in status():
                print(line)
        except EnvironmentError as error:
            message = (
                f'{"#" * 10} [INFO] Status failed ({error}) {"#" * 10}',
                "red")
        else:
            message = (
                f'{"#" * 10} [INFO] Status succeeded {"#" * 10}',
                "green")
        content, color = message
        print(colored(content, color))


class RemoveCommand(AbstractCommand):
    def __init__(self, build_config: BuildConfig):
        super().__init__(build_config, 'remove', 'remove (uninstall) one or more keywords')
        self.mark = AddRemoveHelper(build_config, self.name)

    def execute(self, arguments: list):
        if not(isinstance(arguments, list) and
               all([isinstance(_, str) for _ in arguments])):
            raise ValueError
        self.mark.execute(arguments)


def all_commands(build_config: BuildConfig):
    """
    CURRENT COMMANDS SUPPORTED
    Create and return a list containing one instance of every known
    AbstractCommand, using build_config and state for each.
    """

    if not(isinstance(build_config, BuildConfig)):
        raise ValueError
    # alphabetical order
    return [AddCommand(build_config),
            CustomCommand(build_config),
            DescribeCommand(build_config),
            InitCommand(build_config),
            InstalledCommand(build_config),
            ListCommand(build_config),
            StatusCommand(build_config),
            RemoveCommand(build_config), ]
