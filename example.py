#!/usr/bin/env python3.9

from Tuffix.TuffixPackageManager import TuffixPackageManager
from Tuffix.Keywords import BazelKeyword
from Tuffix.Configuration import DEBUG_BUILD_CONFIG

__T = TuffixPackageManager(None, BazelKeyword(DEBUG_BUILD_CONFIG))
__T.remove_source("deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8")
