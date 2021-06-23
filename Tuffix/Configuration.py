##########################################################################
# configuration
# AUTHOR(S): Kevin Wortman
##########################################################################

from Tuffix.Exceptions import *
from Tuffix.Constants import *

import packaging.version
import pathlib
import json

# Configuration defined at build-time. This is a class so that we can
# unit test with dependency injection.


class BuildConfig:
    """
    version: packaging.Version for the currently-running Tuffix instance
    state_path: pathlib.Path holding the path to the state.json
    json_state_path: pathlib.Path holding the path to custom keyword files
    """

    def __init__(self,
                 version,
                 state_path,
                 json_state_path):
        if not (isinstance(version, packaging.version.Version) and
                isinstance(state_path, pathlib.Path) and
                state_path.suffix == '.json' and
                isinstance(json_state_path, pathlib.Path)):
            raise ValueError
        self.version = version
        self.state_path = state_path
        self.json_state_path = json_state_path  # NOTE

    def __eq__(self, other):
        return (
            self.version == other.version and
            self.state_path == other.state_path and
            self.json_state_path == other.json_state_path
        )


# Singleton BuildConfig object using the constants declared at the top of
# this file.
DEFAULT_BUILD_CONFIG = BuildConfig(VERSION, STATE_PATH, JSON_PATH)


class State:
    """
    Build_config: a BuildConfig object
    Version: packaging.Version for the tuffix version that created this state
    Installed: list of strings representing the codewords that are currently installed

    NOTE: Current state of tuffix, saved in a .json file under /var.
    """

    def __init__(self, build_config, version, installed, editors):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(version, packaging.version.Version) and
                isinstance(installed, list) and
                all([isinstance(codeword, str) for codeword in installed]) and
                isinstance(editors, list) and
                all([isinstance(editor, str) for editor in editors])):
            raise ValueError
        self.build_config = build_config
        self.version = version
        self.installed = installed
        self.editors = editors

    def __eq__(self, other):
        # this might be nice to implement as a dataclass?
        return (
            self.build_config == other.build_config and
            self.version == other.version and
            self.installed == other.installed and
            self.editors == other.editors
        )

    # Write this state to disk.
    def write(self):
        with open(self.build_config.state_path, 'w') as f:
            document = {
                'version': str(self.version),
                'installed': self.installed,
                'editors': self.editors
            }
            json.dump(document, f)


def read_state(build_config):
    """
    Reads the current state of Tuffix.
    build_config: A BuildConfig object.
    raise EnvironmentError if there is a problem
    """

    if not isinstance(build_config, BuildConfig):
        raise ValueError
    try:
        with open(build_config.state_path) as f:
            document = json.load(f)
            return State(build_config,
                         packaging.version.Version(document['version']),
                         document['installed'],
                         document['editors'])
    except (OSError, FileNotFoundError):
        raise EnvironmentError(
            'state file not found, you must run $ tuffix init')
    except json.JSONDecodeError:
        raise EnvironmentError('state file JSON is corrupted')
    except packaging.version.InvalidVersion:
        raise EnvironmentError('version number in state file is invalid')
    except KeyError as e:
        raise EnvironmentError(
            f'state file JSON is missing required keys: {e}')
    except ValueError:
        raise EnvironmentError('state file JSON has malformed values')
