#!/usr/bin/env python3.9

import re
import textwrap
import shutil
import subprocess
import os
# import termcolor


def helper_function(content: str, regex: re.Pattern) -> tuple[str]:
    """
    Match the contents of a given string to the given regex
    Will fail if the regex cannot find anything
    """

    if not(isinstance(content, str) and
           isinstance(regex, re.Pattern)):
        raise ValueError(f'{content=}, {regex=}')

    container = list(regex.groupindex.keys())
    content = textwrap.dedent(content).strip()

    if((_match := regex.search(content)) is None):
        raise ValueError(f'{_match=} is not a valid match (re of {regex=})')

    match container:
        case[_]:
            return _match.groups()
        case _:
            raise ValueError(f'groups not utilized')


def file_matcher(content: str, regexes: list[re.Pattern]) -> list[str]:
    if not(isinstance(content, str) and
           isinstance(regexes, list) and
           all([isinstance(_, re.Pattern) for _ in regexes])):
        raise ValueError

    return [
        helper_function(content, regex) for regex in regexes
    ]


def graphics_information() -> tuple[str]:
    assert((lspci := shutil.which("lspci")) and (bash := shutil.which("bash")))
    _lspci_output = '\n'.join(subprocess.check_output(
        lspci,
        shell=True,
        executable=bash,
        encoding="utf-8",
        universal_newlines="\n").splitlines())

    regexes: list[str] = [
        re.compile("VGA.*\\:(?P<vgacontroller>(?:(?!\\s\\().)*)"),
        re.compile("3D.*\\:(?P<accelerator>(?:(?!\\s\\().)*)")

    ]

    vga, controller = file_matcher(_lspci_output, regexes)
    return (
        *vga,
        *controller
        # termcolor.colored(*vga, 'green'),
        # termcolor.colored(*controller, 'red')
    )


def git_configuration() -> tuple[str]:
    assert((git := shutil.which("git")) and (bash := shutil.which("bash")))
    git_output = '\n'.join(subprocess.check_output(
        f'{git} --no-pager config --list',
        shell=True,
        executable=bash,
        encoding="utf-8",
        universal_newlines="\n").splitlines())

    regexes: list[str] = [
        re.compile("user\\.name\\=(?P<user>.*)"),
        re.compile("user\\.email\\=(?P<email>.*)")

    ]
    user, email = file_matcher(git_output, regexes)

    return (
        *user,
        *email
    )


def system_shell() -> tuple[str]:
    assert((bash := shutil.which("bash")) and (
        user := os.getlogin()) != "root")

    passwd_file = "/etc/passwd"
    if not(os.path.exists(passwd_file)):
        raise EnvironmentError(f'cannot find {passwd_file}, is this unix?')

    with open(passwd_file, "r") as fp:
        content = '\n'.join(fp.readlines())

    regexes: list[str] = [
        re.compile(
            f"{user}\\:x\\:\\d+\\:\\d+\\:+\\/home\\/{user}\\:(?P<path>.*)")
    ]
    shell_path = file_matcher(content, regexes)
    shell_name = os.path.basename(''.join(*shell_path))

    shell_version, _ = subprocess.Popen([''.join(*shell_path), '--version'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        encoding="utf-8").communicate()
    regexes: list[str] = [
        re.compile(f"{shell_name}\\s*[version]?\\s(?P<version>\\d+\\.\\d+)")
    ]
    print(shell_version)
    shell_version = file_matcher(shell_version, regexes)
    print(shell_version)


system_shell()
