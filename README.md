# Tuffix 2: Tuffy's Linux

Tuffix is the official Linux environment for CPSC 120, 121, and 131 at California
State University, Fullerton. Our mascot is Tuffy the elephant.

This version 2 replaces the older tuffix 1 that was at https://github.com/kevinwortman/tuffix .

## Installation Instructions

You probably came here to install Tuffix. To do that, follow the [Installation Instructions wiki page](https://github.com/CSUF-Tuffix/Tuffix-2/wiki/Installation-Instructions).

## Overview

The goal of this effort is to have a unified programming
environment for our introductory courses that is accessible, fosters
collaboration, and enables students and instructors to share 
code and feedback with one another.

The Tuffix environment is an overlay on top of the current Ubuntu LTS release.

`tuffix` is a command-line configuration tool. It manages adding and removing **keywords** from the system. A keyword is a collection of software needed for a course.

Every Tuffix user will want to install the `base` keyword, which supports CPSC 120-121-131, and includes
* clang compiler
* GNU g++9 C++ compiler
* Atom text editor
* gdb debugger and Atom's dgb-gdb frontend

There are additional keywords for other courses and activities. For example, the `240` keyword supports CPSC 240, and the `latex` keyword supports writing LaTeX documents (e.g. research papers).

## Community Slack Workspace

Anyone using Tuffix (students, instructors, developers) should join the
[CSUF TUFFIX](https://csuf-tuffix.slack.com)
slack workspace at
[https://csuf-tuffix.slack.com](https://csuf-tuffix.slack.com).

Please use the appropriate channel within the workspace:

* `#general`: Troubleshooting installing and using Tuffix. This is
  usually the right place for students to ask questions. Open to
  anyone with a CSUF account.
  
* `#instructors`: Troubleshooting instructor's issues, such as setting
  up classes or assignments with Tuffix. This is only open to CSUF
  instructors. If you are a CSUF instructor, please ask a Slack
  workspace admin to invite you to the `#instructors` channel.

* `#developers`: Creating and maintaining the Tuffix system. This is
  only open to people who are actively contributing to the Tuffix
  project (mostly instructors). If you are interested in being a
  developer, please ask a Slack workspace admin, or current developer,
  to invite you to the `#developers` channel.

## Acknowledgements

This is the product of a working group including but not limited to Jared Dyreson, Paul
Inventado, Michael Shafae, and Kevin Wortman. It builds upon Michael Shafae's build
scripts and Kenytt Avery's
node-box (https://github.com/ProfAvery/node-box).
