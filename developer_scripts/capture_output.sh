#!/usr/bin/env bash

# example logger script
# Author: Jared Dyreson


LOG_DIR="tuffix_logs"
TEST_DIR="/home/jared/Projects/TuffixConglomerate/Tuffix-Lib/UnitTests"

function __test_dne() {
    echo "[ERROR] Unable to conduct test $1, does not exist"
    exit
}

[[ -z "$@" ]] && exit

[[ ! -d  "$LOG_DIR" ]] && mkdir "$LOG_DIR"

for __test in "$@"; do
    [[ ! -d  ""$TEST_DIR"/$__test" ]] && (__test_dne $__test)
    exec 1> >(tee ""$LOG_DIR"/"$__test"_tuffix_stdout.log")
    exec 2> >(tee ""$LOG_DIR"/"$__test"_tuffix_stderr.log")
    sudo python3 runner.py --test "$__test"
done

