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
TEST_CASES = ['test_missing_file', 'test_main_output', 'test_output_file', 'test_adds', 'test_deletes']
#TEST_CASES = ['test_ls', 'test_path']

#--------------------------------------------------------------------------
# Global variables - modify as needed
#--------------------------------------------------------------------------
PARENT_PROJECT = '../..'
PROJECT = 'LinkedList_Project_AutoTest'
BUILD = 'build'
TEST_DIR = os.path.join(PROJECT, BUILD)
EXECUTABLE = './main'
#DIFF = 'diff --ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --suppress-common-lines --color=always'
DIFF = 'diff --ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --color=always'

DATA_DIR = '..'
TESTDATAFILES = ['AutoTest_mymovies.txt', 'AutoTest_add_movies.txt', 'AutoTest_del_movies.txt']
DATAFILES = ['mymovies.txt', 'add_movies.txt', 'del_movies.txt']

AUTOTEST_MAIN_MISSING_FILE = 'AutoTest_main_missing_file.txt'
STUDENT_MAIN_MISSING_FILE = 'test_main_missing_file.txt'

AUTOTEST_MAIN_OUTPUT_FILE = 'AutoTest_main_output.txt'
STUDENT_MAIN_OUTPUT_FILE = 'test_main_output.txt'

AUTOTEST_MOVIE_UPDATE_FILE = 'AutoTest_mymovies_updated.txt'
STUDENT_MOVIE_UPDATE_FILE = 'mymovies_updated.txt'

AUTOTEST_ADD_MOVIES_FILE = 'AutoTest_add_movies.txt'
AUTOTEST_DEL_MOVIES_FILE = 'AutoTest_del_movies.txt'

#--------------------------------------------------------------------------
# Font colors for terminal output
#--------------------------------------------------------------------------
BLUE = '\033[34m'
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'


def report_failure(msg):
    """
    Prints a failure message in red font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{RED}[----------]{RESET}')
    print(f'{RED}[  FAILED  ] {msg}{RESET}')
    print(f'{RED}[----------]{RESET}')
    return

def report_success(msg):
    """
    Prints a success message in green font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{GREEN}[----------]{RESET}')
    print(f'{GREEN}[  PASSED  ] {msg}{RESET}')
    print(f'{GREEN}[----------]{RESET}')
    return

def report_info(msg, color=RESET):
    """
    Prints an informational message in the specified font color.
    Parameters:
         msg (str): The message to print.
         color (str): The font color to use. Defaults to GREEN.
    Returns:
         None
    """
    print(f'{color}{msg}{RESET}')
    return



#--------------------------------------------------------------------------
# Helper functions
#--------------------------------------------------------------------------

def execute_command(cmd, args=None, accept_rc=[0]):
    """
    Executes a shell command and provides verbose and debug output based on the given arguments.
    Parameters:
         cmd (str): The shell command to execute.
         args (object, optional): An object containing verbose and debug flags. Defaults to None.
         accept_rc (list, optional): A list of acceptable return codes. Defaults to [0].
    Returns:
         int: The return code of the executed command.
    Behavior:
    - If `args.verbose` is True, prints the command execution details.
    - If `args.debug` is False, executes the command using `subprocess.call`.
    - If `args.verbose` is True, prints the result of the command execution, including specific messages for segmentation faults (rc=139) and uncaught exceptions (rc=134).
    """
    rc = 0

    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'{GREEN}[==========]{RESET}')
        print(f'{GREEN}[ EXECUTE  ] {cmd}{RESET}')
        print(f'{GREEN}[==========]{RESET}')

    if not args.debug:
        rc = subprocess.call(cmd, shell=True)

    if args.verbose:
        if rc == 139:
            report_failure('Segmentation Fault')
        elif rc == 134:
            report_failure('Uncaught Exception')
        elif rc not in accept_rc:
            report_failure(f'rc = {rc}')
        else:
            report_success(f'rc = {rc}')
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
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_MISSING_FILE} 2>&1'
    rc = execute_command(cmd, args, accept_rc=[0,1])

    # compare the output
    cmd = f'{DIFF} {os.path.join(DATA_DIR, AUTOTEST_MAIN_MISSING_FILE)} {STUDENT_MAIN_MISSING_FILE}'
    rc = execute_command(cmd, args)
    return rc

def test_main_output(args):
    if (copy_test_input_files() != 0):
        return 1

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE} 2>&1'
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
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE} 2>&1'
    rc = execute_command(cmd, args)

    # compare the output
    cmd = f'{DIFF} {os.path.join(DATA_DIR, AUTOTEST_MOVIE_UPDATE_FILE)} {STUDENT_MOVIE_UPDATE_FILE}'
    rc = execute_command(cmd, args)
    return rc

def check_lines(search_file, target_file, check_existence=True):
    """
    Checks if all lines from the search file exist or do not exist in the target file 
    based on the check_existence flag.

    Args:
        search_file (str): The path to the file containing lines to search for.
        target_file (str): The path to the file where lines are being searched.
        check_existence (bool): If True, checks if all lines exist in the target file. 
                                If False, checks if all lines do not exist in the target file.
                                Defaults to True.
    Returns:
        bool: True if the condition specified by check_existence is met, False otherwise.

    Prints:
        - A message indicating whether the condition specified by check_existence is met.
        - If there are lines that do not meet the condition, prints each such line.
        - An error message if either file is not found.
    """
    try:
        with open(search_file, 'r') as sf, open(target_file, 'r') as tf:
            search_lines = set(sf.readlines())
            target_lines = set(tf.readlines())
            
            if check_existence:
                missing_lines = search_lines - target_lines
                if missing_lines:
                    print(f"Missing lines in {target_file}:")
                    for line in missing_lines:
                        print(line.strip())
                    return False
                else:
                    print(f"All lines from {search_file} exist in {target_file}.")
                    return True
            else:
                existing_lines = search_lines & target_lines
                if existing_lines:
                    print(f"Lines from {search_file} that exist in {target_file}:")
                    for line in existing_lines:
                        print(line.strip())
                    return False
                else:
                    print(f"No lines from {search_file} exist in {target_file}.")
                    return True
    except FileNotFoundError as e:
        report_failure(f'Search or target file not found. {e}')
        return False


def test_adds(args):
    if (copy_test_input_files() != 0):
        report_failure('Unable to copy test files.')
        return 1

    # make sure the movie update file does NOT exist
    if os.path.exists(STUDENT_MOVIE_UPDATE_FILE):
        os.remove(STUDENT_MOVIE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE} 2>&1'
    rc = execute_command(cmd, args)

    # compare the output
    if not check_lines(os.path.join(DATA_DIR, AUTOTEST_ADD_MOVIES_FILE), STUDENT_MOVIE_UPDATE_FILE):
        report_failure('Add movies failed.')
        rc = 1
    else:
        report_success('Add movies passed.')
        rc = 0
    return rc

def test_deletes(args):
    if (copy_test_input_files() != 0):
        report_failure('Unable to copy test files.')
        return 1

    # make sure the movie update file does NOT exist
    if os.path.exists(STUDENT_MOVIE_UPDATE_FILE):
        os.remove(STUDENT_MOVIE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_OUTPUT_FILE} 2>&1'
    rc = execute_command(cmd, args)

    # compare the output
    if not check_lines(os.path.join(DATA_DIR, AUTOTEST_DEL_MOVIES_FILE), STUDENT_MOVIE_UPDATE_FILE, check_existence=False):
        report_failure('Delete movies failed.')
        rc = 1
    else:
        report_success('Delete movies passed.')
        rc = 0
    return rc

#--------------------------------------------------------------------------
# Everything below this line is generic code to execute tests defined above
# Do not modify anything below this line
#--------------------------------------------------------------------------
def banner(msg, args):
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   TEST   ] {msg}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

def footer(msg, rc, args):
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   END    ] {msg} rc: {rc}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

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
