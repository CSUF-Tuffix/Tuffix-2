##########################################################################
# constants
# AUTHOR: Kevin Wortman
##########################################################################

import packaging.version
import pathlib

VERSION = packaging.version.parse("0.1.0")

STATE_PATH = pathlib.Path("/var/lib/tuffix/state.json")
JSON_PATH = pathlib.Path("/var/lib/tuffix/json_payloads")

DEBUG_STATE_PATH = pathlib.Path("/tmp/tuffix/state.json")
DEBUG_JSON_PATH = pathlib.Path("/tmp/tuffix/json_payloads")

KEYWORD_MAX_LENGTH = 8

DEBUG = False
