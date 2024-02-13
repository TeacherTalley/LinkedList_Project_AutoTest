#!/usr/bin/env python
#--------------------------------------------------------------------------
# File: AutoTest_OutputTest.py
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
import sys
import os
import subprocess
import shutil
import argparse


#--------------------------------------------------------------------------
# list all test cases to be executed here - modify as needed
#--------------------------------------------------------------------------
TEST_CASES = ['test_missing_file', 'test_main_output', 'test_output_file']
#TEST_CASES = ['test_ls', 'test_path']

#--------------------------------------------------------------------------
# Global variables - modify as needed
#--------------------------------------------------------------------------
PARENT_PROJECT = '../..'
PROJECT = 'LinkedList_Project_AutoTest'
BUILD = 'build'
TEST_DIR = os.path.join(PROJECT, BUILD)
EXECUTABLE = './main'
DIFF = 'diff --ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --suppress-common-lines --color=always'

DATA_DIR = '..'
TESTDATAFILES = ['AutoTest_mymovies.txt', 'AutoTest_add_movies.txt', 'AutoTest_del_movies.txt']
DATAFILES = ['mymovies.txt', 'add_movies.txt', 'del_movies.txt']

AUTOTEST_MAIN_MISSING_FILE = 'AutoTest_main_missing_file.txt'
STUDENT_MAIN_MISSING_FILE = 'test_main_missing_file.txt'

AUTOTEST_MAIN_OUTPUT_FILE = 'AutoTest_main_output.txt'
STUDENT_MAIN_OUTPUT_FILE = 'test_main_output.txt'

AUTOTEST_MOVIE_UPDATE_FILE = 'AutoTest_mymovies_updated.txt'
STUDENT_MOVIE_UPDATE_FILE = 'mymovies_updated.txt'

#--------------------------------------------------------------------------
# Helper functions
#--------------------------------------------------------------------------

def execute_command(cmd, args=None):
    rc = 0

    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'Executing: {cmd}')
    if not args.debug:
        rc = subprocess.call(cmd, shell=True)
    return rc

#--------------------------------------------------------------------------
# Test functions - Add your test functions here
#
# setup(args) - function to execute before running tests
# cleanup(args) - function to execute after running tests
#--------------------------------------------------------------------------

def setup(args):
    cwd = os.getcwd()
    if not cwd.endswith(TEST_DIR):
        try:
            os.chdir(TEST_DIR)
        except:
            print(f'ERROR: Unable to change directory to: {TEST_DIR}')
            sys.exit(1)
    if args.debug:
        print(f'\nsetup: Changed directory to: {os.getcwd()}')
    return

def cleanup(args):
    cwd = os.getcwd()
    if cwd.endswith(TEST_DIR):
        try:
            os.chdir(PARENT_PROJECT)
        except:
            print(f'ERROR: Unable to change directory to: {".."}')
            sys.exit(1)
    if args.debug:
        print(f'\ncleanup: Changed directory to: {os.getcwd()}')
    return

def test_ls(args):
    cmd = f'ls -l'
    rc = execute_command(cmd, args)
    return rc

def test_path(args):
    cmd = f'echo $PATH'
    rc = execute_command(cmd, args)
    return rc

def copy_test_input_files():
    # make sure the data files exist
    for file, testfile in zip(DATAFILES, TESTDATAFILES):
        if not os.path.exists(file):
            try:
                shutil.copyfile(os.path.join(DATA_DIR, testfile), file)
            except:
                print(f'ERROR: Unable to copy {os.path.join(DATA_DIR, testfile)} to {os.getcwd()}')
                return 1
    return 0

def test_missing_file(args):
    # make sure the data files do NOT exist
    for file in DATAFILES:
        if os.path.exists(file):
            os.remove(file)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_MISSING_FILE}'
    rc = execute_command(cmd, args)

    # compare the output
    cmd = f'{DIFF} {os.path.join(DATA_DIR, AUTOTEST_MAIN_MISSING_FILE)} {STUDENT_MAIN_MISSING_FILE}'
    rc = execute_command(cmd, args)
    return rc

def test_main_output(args):
    if (copy_test_input_files() != 0):
        return 1

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE}'
    rc = execute_command(cmd, args)

    # compare the output
    cmd = f'{DIFF} {os.path.join(DATA_DIR, AUTOTEST_MAIN_OUTPUT_FILE)} {STUDENT_MAIN_OUTPUT_FILE}'
    rc = execute_command(cmd, args)
    return rc

def test_output_file(args):
    if (copy_test_input_files() != 0):
        return 1

    # make sure the movie update file does NOT exist
    if os.path.exists(STUDENT_MOVIE_UPDATE_FILE):
        os.remove(STUDENT_MOVIE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE}'
    rc = execute_command(cmd, args)

    # compare the output
    cmd = f'{DIFF} {os.path.join(DATA_DIR, AUTOTEST_MOVIE_UPDATE_FILE)} {STUDENT_MOVIE_UPDATE_FILE}'
    rc = execute_command(cmd, args)
    return rc

#--------------------------------------------------------------------------
# Everything below this line is generic code to execute tests defined above
# Do not modify anything below this line
#--------------------------------------------------------------------------
def banner(msg, args):
    if args.verbose:
        print(f'\n{"-"*10} TEST: {msg} {"-"*40}\n')

def footer(msg, rc, args):
    if args.verbose:
        print(f'\n{"-"*10} END: {msg} rc: {rc} {"-"*35}\n') 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=True, 
                        help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, 
                        help="Enable quiet mode")
    parser.add_argument("--nosetup", action="store_true", default=False, 
                        help="Disable setup before running tests")
    parser.add_argument("--nocleanup", action="store_true", default=False, 
                        help="Disable cleanup after running tests")
    parser.add_argument("--debug", action="store_true", default=False, 
                        help="Enable debug mode")
    parser.add_argument("-t", "--test", nargs='+', type=str, default=None, 
                        help=f"Specify the test(s) to run from: {TEST_CASES}")
    return parser.parse_args()

def test_main():
    args = parse_arguments()

    if args.quiet:
        args.verbose = False

    if not args.nosetup:
        # execute the setup function if it exists
        try:
            setup(args)
        except NameError:
            pass

    # if no test ID is provided, run all tests
    if not args.test:
        tests = TEST_CASES
    else:
        tests = args.test

    if args.verbose:
        print(f"\nRunning tests: {tests}...\n")
    for test in tests:
        banner(test, args)
        try:
            rc = globals()[test](args)
        except NameError:
            print(f"ERROR: Test function {test} not found.")
            rc = 0
        footer(test, rc, args)

    if not args.nocleanup:
        # execute the cleanup function if it exists
        try:
            cleanup(args)
        except NameError:
            pass

    sys.exit(rc)

def main():
    test_main()

if __name__ == "__main__":
    main()
