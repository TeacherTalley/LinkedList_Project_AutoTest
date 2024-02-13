#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_Style.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
project="LinkedList_Project_AutoTest"
pip install cpplint
cd $project

srcfiles="main.cpp"
echo "Source files:" $srcfiles

# for some reason, GitHub Classroom environment does not use cpplint.cfg
# explcitly ignore some style checks
filters=-legal/copyright,-build/header_guard,-whitespace/braces,-runtime/explicit,\
-whitespace/newline,-whitespace/end_of_line,-whitespace/blank_line,\
-whitespace/indent,-whitespace/comments,-runtime/string,-whitespace/line_length,\
-whitespace/parens,-readability/todo,-readability/braces

cpplint --filter=$filters $srcfiles