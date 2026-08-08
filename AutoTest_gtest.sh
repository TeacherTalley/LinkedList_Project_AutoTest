#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_gtest.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
# GTest does not report segmentation faults as errors when running a single test.
# This script runs the individual tests and reports an error for any test
# with a non-zero exit code.
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

script_name=$(basename "$0")
script_dir=$(dirname "$0")

if [ $# -eq 3 ]; then
  verbose=$3
else
  verbose=0
fi

if [ $# -lt 1 ]; then
  echo "Usage: $script_name <test_executable> [--gtest_filter=<test_name> | <test_name>]"
  exit 1
fi

# If test executable is not specified, guess the name and location of the gtest executable
if [ $# -eq 1 ]; then
  test_executable="${script_dir}/build/AutoTest_gtests"
  test_selection=$1
else
  test_executable=$1
  test_selection=$2
fi

if [[ $test_selection == --gtest_filter=* ]]; then
  test_name=$(echo $test_selection | awk -F'=' '{print $2}')
else
  test_name=$test_selection
fi

# Run the test
if [ $verbose -ne 0 ]; then
  printf "${green}[==========]${reset}\n"
  printf "${green}[  RUN     ] ${test_executable} --gtest_filter=${test_name}${reset}\n"
  printf "${green}[==========]${reset}\n" 
fi
$test_executable --gtest_filter=$test_name
rc=$?

if [ $rc -ne 0 ]; then
  if [ $rc -eq 139 ]; then
    reason="(Segmentation Fault)"
  elif [ $rc -eq 134 ]; then
    reason="(Uncaught Exception)"
  else
    reason="(Failed with exit code $rc)"
  fi

  testname=$(echo $test_selection | awk -F'=' '{print $2}')
  printf "${red}[===========]${reset}\n"
  printf "${red}[ ❌ FAILED ] ${test_name}: ${reason}${reset}\n"
  printf "${red}[===========]${reset}\n"
fi

exit $rc