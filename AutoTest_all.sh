#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_all.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
repo=LinkedList_Project_AutoTest
echo "#################### START: AutoTest Setup ##################################"
echo " To be consistent with the grading environment, assume we are starting out "
echo " in the source directory (i.e., the parent of the AutoTest directory)."
echo " You will get a cd error if you execute directly from the AutoTest directory."
echo "#############################################################################"
cd $repo
echo "#################### START: AutoTest Results #####################"
./$project/AutoTest_Style.sh $repo main.cpp
echo
echo "--- Output Testing ---"
cd ..
./$repo/AutoTest_OutputTest.py --test test_missing_file
./$repo/AutoTest_OutputTest.py --test test_main_output
./$repo/AutoTest_OutputTest.py --test test_output_file
./$repo/AutoTest_OutputTest.py --test test_adds
./$repo/AutoTest_OutputTest.py --test test_deletes
echo
echo "#################### END: AutoTest Results   #####################"
echo
