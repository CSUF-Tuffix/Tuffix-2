#!/usr/bin/env python3.9

from Tuffix.TuffixPackageManager import TuffixPackageManager
from Tuffix.Keywords import C240Keyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

__T = TuffixPackageManager(None, C240Keyword(DEBUG_BUILD_CONFIG))
__T.install("cowsay")
