#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_all.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
echo "#################### START: AutoTest Results #####################"
project="LinkedList_Project_AutoTest"
# Assume running from parent directory as with GitHub Classroom tests
cd ..
echo
echo "--- Checking code format (cpplint) ---"
./$project/AutoTest_Style.sh
echo
echo "--- Output Testing ---"
./$project/AutoTest_OutputTest.py --test test_missing_file
./$project/AutoTest_OutputTest.py --test test_main_output
./$project/AutoTest_OutputTest.py --test test_output_file
echo
echo "#################### END: AutoTest Results   #####################"
echo
