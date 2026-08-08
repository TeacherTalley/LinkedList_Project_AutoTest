#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_setup.sh
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

if [ -n "$1" ]; then # if argument specified, use source from that directory
    basepath="$1"
    # Remove trailing slash if it exists
    basepath="${basepath%/}"
else
    basepath=".."
fi
# Check if additional source files are provided as arguments
if [ $# -gt 1 ]; then
    srcfiles="${@:2}"
    # Prepend basepath to each file in srcfiles
    srcfiles=$(echo $srcfiles | sed "s|[^ ]*|$basepath/&|g")
else
    srcfiles="$basepath/main.cpp $basepath/*.h"
fi

printf "${green}[==========]${reset}\n"
printf "${green}[ SETUP    ] Source directory: ${basepath}${reset}\n"
printf "${green}[          ] Source files: ${srcfiles}${reset}\n"
printf "${green}[          ] Copying files.${reset}\n"
printf "${green}[----------]${reset}\n"
cp $srcfiles .
rc=$?

printf "${green}[==========]${reset}\n"
printf "${green}[ COMPILE  ] Compiling program.${reset}\n"
printf "${green}[----------]${reset}\n"
if [ -d "build" ]; then
    rm -rf build
fi
cmake -S . -B build
cmake --build build
rc=$?
if [ $rc -ne 0 ]; then
    printf "${red}[===========]${reset}\n"
    printf "${red}[ ❌ FAILED ] Compile failed. Grade penalty to be assessed.${reset}\n"
    printf "${red}[===========]${reset}\n"
else
    printf "${green}[===========]${reset}\n"
    printf "${green}[ ✅ PASSED ] Compile successful.${reset}\n"
    printf "${green}[===========]${reset}\n"
fi
exit $rc
