#!/bin/bash
pip install cpplint
cd LinkedList_Project

srcfiles="main.cpp"
echo "Source files:" $srcfiles

# for some reason, GitHub Classroom environment does not use cpplint.cfg
# explcitly ignore some style checks
filters=-legal/copyright,-build/header_guard,-whitespace/braces,-runtime/explicit,\
-whitespace/newline,-whitespace/end_of_line,-whitespace/blank_line,\
-whitespace/indent,-whitespace/comments,-runtime/string

cpplint --filter=$filters $srcfiles