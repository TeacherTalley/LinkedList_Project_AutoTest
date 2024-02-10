#!/bin/bash
echo
echo "#################### START: AutoTest Results #####################"
echo
echo "--- Checking code format (cpplint) ---"
./AutoTest_Style.sh
echo
echo "--- Output Testing ---"
./AutoTest_OutputTest.py --test test_missing_file
./AutoTest_OutputTest.py --test test_main_output
./AutoTest_OutputTest.py --test test_output_file

echo
echo "#################### END: AutoTest Results   #####################"
echo
