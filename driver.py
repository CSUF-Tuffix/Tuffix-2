#!/usr/bin/env python3.9

"""
Official driver code for Tuffix
Author(s): Jared Dyreson, Kevin Wortman
"""


# from Tuffix.Driver import *

import sys


def help_message(i: int):
    print(f"received {i} argument(s), cowardly refusing")


if((argc := len(sys.argv)) < 2):
    help_message(argc)
    quit()

# main(sys.argv[1:])
