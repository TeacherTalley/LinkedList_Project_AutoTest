#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_Style.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------


# force color output in test harnesses
# if using a terminal that does not support color, you can disable color output 
# by setting the following FORCE_COLOR and CLICOLOR_FORCE environment variables to 0
# Classroom 50 JSON auto-grading environment does not support color output, 
# so we disable it here.
export FORCE_COLOR=0
export CLICOLOR_FORCE=0

# Test FORCE_COLOR and set color variables accordingly
# See: https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
if [ "$FORCE_COLOR" = "1" ]; then
  red="\033[31m"
  green="\033[32m"
  blue="\033[34m"
  reset="\033[0m"
else
  red=""
  green=""
  blue=""
  reset=""
fi

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <test_directory> <source_files...>"
    exit 1
fi

test_directory=$1
shift
srcfiles="$@"

printf "${green}[==========]${reset}\n"
printf "${green}[ STYLE    ] Checking ${srcfiles}${reset}\n"
printf "${green}[----------]${reset}\n"

pip install cpplint

cd "$test_directory"

# for some reason, GitHub Classroom environment does not use cpplint.cfg
# explcitly ignore some style checks
filters=-legal/copyright,-build/header_guard,\
-runtime/explicit,,-runtime/string,-runtime/references,\
-readability/todo,-readability/braces,\
-whitespace/newline,-whitespace/end_of_line,-whitespace/blank_line,\
-whitespace/indent,-whitespace/comments,-whitespace/line_length,\
-whitespace/ending_newline,-whitespace/braces

cpplint --filter=$filters $srcfiles
rc=$?

if [ $rc -ne 0 ]; then
  printf "${red}[===========]${reset}\n"
  printf "${red}[ ❌ FAILED ] Coding style checks.${reset}\n"
  printf "${red}[===========]${reset}\n"
else
  printf "${green}[===========]${reset}\n"
  printf "${green}[ ✅ PASSED ] Coding style checks${reset}\n"
  printf "${green}[===========]${reset}\n"
fi
exit $rc
