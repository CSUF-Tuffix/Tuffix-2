#!/usr/bin/env python3.9

"""
Experimental usage of the Tuffix API to be used as auto
install scripts to supersede `thin-mint`

NOTE: once Tuffix is fully released and I am no longer a maintainer, `apt` will be
replaced with `pacman`, as my systems will be running some sort of Arch Linux

TODO:

- Create package manager class, which can be filled in
  once the repository is forked. This will be considered a template
  for other universities, if they chose to use Redhat, PopOS! or some other flavour of Linux

"""

from Tuffix.Commands import InitCommand
from Tuffix.Configuration import DEFAULT_BUILD_CONFIG, State
from Tuffix.Editors import VimKeyword

# can be redefined as ThinMintInstallerCommand

init_command = InitCommand(DEFAULT_BUILD_CONFIG)
new_state = State(DEBUG_BUILD_CONFIG,
                  DEBUG_BUILD_CONFIG.version,
                  [], [])
init_command.create_state_directory()
new_state.write()
