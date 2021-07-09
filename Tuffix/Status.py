##########################################################################
# status API
# AUTHORS: Jared Dyreson, Kevin Wortman
##########################################################################

"""
Used for managing code execution by one user on the behalf of another
For example: root creating a file in Jared's home directory but Jared is still the sole owner of the file
We probably should instantiate a global SudoRun instead of re running it everytime in each function it's used in
^ This is going to be put inside the SiteConfig and BuildConfig later so it can be referenced for unit testing

NOTE: update this section with https://github.com/JaredDyreson/SudoRun/
"""

from Tuffix.SudoRun import SudoRun
from Tuffix.Configuration import read_state, DEFAULT_BUILD_CONFIG
from Tuffix.Exceptions import *

from termcolor import colored
import datetime
import os
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import termcolor

def ensure_ubuntu():
    """
    /etc/debian_release -> /etc/debian_version
    """

    if not(os.path.exists("/etc/debian_version")):
        raise UsageError(
            'this is not an Debian derivative, please try again')


def ensure_root_access():
    """
    Raises UsageError if we do not have root access.
    """

    if(os.getuid() != 0):
        raise UsageError(
            'you do not have root access; run this command like $ sudo tuffix ...')


def in_VM() -> bool:
    """
    Goal: check if we're in a VM
    SOURCE: https://www.kite.com/python/answers/how-to-determine-if-code-is-being-run-inside-a-virtual-machine-in-python
    """

    return hasattr(sys, 'real_prefix')


def cpu_information() -> str:
    """
    Goal: get current CPU model name and the amount of cores
    """

    path = pathlib.Path("/proc/cpuinfo")
    regexes: list[re.Pattern] = [
        re.compile("cpu cores\s*\:\s*(?P<cores>[\d]+)"),
        re.compile("model name\s*\:\s*(?P<cpuname>.*)")
    ]

    with open(path, "r") as fp:
        contents = ''.join(fp.readlines())

    cores, name = [
        match.group(1) for regex in regexes if((match := regex.search(contents)))
    ]

    return f'{name} ({cores} core(s))'


def host() -> str:
    """
    Goal: get the current user logged in and the computer they are logged into
    """

    return f"{os.getlogin()}@{socket.gethostname()}"


def current_operating_system() -> str:
    """
    Goal: get current Linux distribution name
    """

    path = pathlib.Path("/etc/os-release")

    if not(path.is_file()):
        raise EnvironmentError(f'Could not find {path}; is this Unix?')

    _re = re.compile("NAME\\=\"(?P<release>[a-zA-Z].*)\"")

    with open(path, "r") as fp:
        contents = ''.join(fp.readlines())

    if not((match := _re.search(contents))):
        raise ParsingError(f'Failed to parse {path}')

    return match.group("release")


def current_kernel_revision() -> str:
    """
    Goal: get the current kernel version
    """

    return os.uname().release


def current_time() -> str:
    """
    Goal: return the current date and time
    """

    return datetime.datetime.now().strftime("%a %d %B %Y %H:%M:%S")


def current_model() -> str:
    """
    Goal: retrieve the current make and model of the host
    """

    product_name = "/sys/devices/virtual/dmi/id/product_name"
    product_family = "/sys/devices/virtual/dmi/id/product_family"
    vendor_name = "/sys/devices/virtual/dmi/id/sys_vendor"

    if not(
            os.path.exists(product_name) or
            os.path.exists(product_family) or
            os.path.exists(vendor_name)):
        raise EnvironmentError(f'could not find system information files')

    with open(product_name, "r") as pn, open(product_family, "r") as pf, open(vendor_name, "r") as vn:
        name = pn.readline().strip('\n')
        family = pf.readline().strip('\n')
        vendor = vn.readline().strip('\n')

    vendor = "" if vendor in name else vendor
    family = "" if name not in family else family
    return f"{vendor} {name}{family}"


def current_uptime() -> str:
    """
    Goal: pretty print the contents of /proc/uptime
    Source: https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
    """

    path = "/proc/uptime"
    if not(os.path.exists(path)):
        raise EnvironmentError(f'could not open {path}, is this unix?')

    with open(path, 'r') as f:
        total_seconds = float(f.readline().split()[0])

    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    days = int(total_seconds / DAY)
    hours = int((total_seconds % DAY) / HOUR)
    minutes = int((total_seconds % HOUR) / MINUTE)
    seconds = int(total_seconds % MINUTE)

    return f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"


def memory_information() -> int:
    """
    Goal: get total amount of ram on system
    """

    def formatting(quantity, power): return quantity / (1000**power)
    path = "/proc/meminfo"
    if not(os.path.exists(path)):
        raise EnvironmentError(f'could not open {path}, is this unix?')

    with open(path, "r") as fp:
        total = int(fp.readline().split()[1])

    return int(formatting(total, 2))


def graphics_information() -> tuple:
    """
    Use lspci to get the current graphics card in use
    Requires pciutils to be installed (seems to be installed by default on Ubuntu)
    Source: https://stackoverflow.com/questions/13867696/python-in-linux-obtain-vga-specifications-via-lspci-or-hal
    """

    regexes: list[re.Pattern] = [
        re.compile(
            "VGA.*\\:\s*(?P<model>(?:(?!\\s\\().)*)")
    ]

    if not((bash := shutil.which("bash")) and
           (lspci := shutil.which("lspci"))):
        raise EnvironmentError(
            f'could not find bash ({bash}) or lspci ({lspci})')

    output = '\n'.join(subprocess.check_output(
        lspci,
        shell=True,
        executable=bash,
        encoding="utf-8",
        universal_newlines="\n").splitlines())

    primary = [
        match.group(1) for regex in regexes if ((match := regex.search(output)))
    ]
    secondary = None # this is currently here because sometimes users might not have 3D accelerated graphics

    return (termcolor.colored(*primary, 'green'),
            termcolor.colored("None" if not secondary else secondary, 'red'))


def list_git_configuration() -> list:
    """
    Retrieve Git configuration information about the current user
    """
    keeper = SudoRun()

    if not((git := shutil.which("git"))):
        raise EnvironmentError(f'could not find git path')

    regexes: list[re.Pattern] = [
        re.compile("user\.email\=(?P<email>.*)"),
        re.compile("user\.name\=(?P<name>.*)")
    ]

    output = '\n'.join(keeper.run(
        command=f"{git} --no-pager config --list",
        desired_user=keeper.whoami))

    return [
        match.group(1) if ((match := regex.search(output))) else "None" for regex in regexes
    ]


def has_internet() -> bool:
    """
    i dont think throwing exception if no internet is good
    setting as bool for unit tests
    """

    PARENT_DIR = '/sys/class/net'
    LOOPBACK_ADAPTER = 'lo'
    ADAPTER_PATH = f'{PARENT_DIR}/{LOOPBACK_ADAPTER}'

    if not(os.path.isdir(PARENT_DIR)):
        raise EnvironmentError(
            f'no {PARENT_DIR}; this does not seem to be Linux')

    carrier_path = f'{ADAPTER_PATH}/carrier'

    if not(os.path.exists(carrier_path)):
        return False

    with open(carrier_path, 'r') as fp:
        state = int(fp.read())
        if(state != 0):
            return True
    return False


def currently_installed_targets() -> list:
    """
    GOAL: list all installed codewords in a formatted list
    """

    return [
        f'{"- ": >4} {element}' for element in read_state(DEFAULT_BUILD_CONFIG).installed]


def status() -> tuple:
    """
    GOAL: Driver code for all the components defined above
    """

    git_email, git_username = list_git_configuration()
    primary, secondary = graphics_information()
    installed_targets = currently_installed_targets()
    installed_targets = '\n'.join(installed_targets).strip() if (
        installed_targets) else "None"

    return (
        f'{host()}',
        '-----',
        f'OS: {current_operating_system()}',
        f'Model: {current_model()}',
        f'Kernel: {current_kernel_revision()}',
        f'Uptime: {current_uptime()}',
        f'Shell: {system_shell()}',
        f'Terminal: {system_terminal_emulator()}',
        f'CPU: {cpu_information()}',
        'GPU:',
        f'  - Primary: {primary}',
        f'  - Secondary: {secondary}',
        f'Memory: {memory_information()} GB',
        f'Current Time: {current_time()}',
        'Git Configuration:',
        f'  - Email: {git_email}',
        f'  - Username: {git_username}',
        'Installed keywords:',
        f'{installed_targets}',
        f'Connected to Internet: {"Yes" if has_internet() else "No"}'
    )


def system_shell() -> str:
    """
    Goal: find the current shell of the user, rather than assuming they are using Bash
    """

    passwd_file = "/etc/passwd"
    if not(os.path.exists(passwd_file)):
        raise EnvironmentError(f'cannot find {passwd_file}, is this unix?')

    current_user = os.getlogin()
    _r_shell = re.compile(
        f"^{current_user}.*\\:\\/home\\/{current_user}\\:(?P<path>.*)")
    shell_name, shell_path, shell_version = None, None, None

    with open(passwd_file, "r") as fp:
        contents = fp.readlines()
    for line in contents:
        shell_match = _r_shell.match(line)
        if(shell_match):
            shell_path = shell_match.group("path")
            shell_version, _ = subprocess.Popen([shell_path, '--version'],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT,
                                                encoding="utf-8").communicate()
            shell_name = os.path.basename(shell_path)

    if not(shell_name or shell_path or shell_version):
        raise EnvironmentError(f'could not parse {passwd_file}')

    _version_re = re.compile("(version)?\\s*(?P<version>[\\w|\\W]+)")
    _version_match = _version_re.match(shell_version)

    if(_version_match):
        return f'{shell_name} {_version_match.group("version")}'
    raise ValueError(
        f'error in parsing version, currently have {shell_version}')


def system_terminal_emulator() -> str:
    """
    Goal: find the default terminal emulator
    Source: https://unix.stackexchange.com/questions/264329/get-the-terminal-emulator-name-inside-the-shell-script
    This is some next level stuff
    """

    _command = """
    sid=$(ps -o sid= -p "$$")
    sid_as_integer=$((sid)) # strips blanks if any
    session_leader_parent=$(ps -o ppid= -p "$sid_as_integer")
    session_leader_parent_as_integer=$((session_leader_parent))
    emulator=$(ps -o comm= -p "$session_leader_parent_as_integer")
    echo "$emulator"
    """

    keeper = SudoRun()

    output = keeper.run(command=_command, desired_user=keeper.whoami)

    if not(output):
        raise ValueError('error when parsing ps output')
    return ' '.join(output)
