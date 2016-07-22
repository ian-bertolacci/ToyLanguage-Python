#!/bin/python
import unittest, tests, yaml, argparse, subprocess, importlib, sys, os, inspect
# Import local unittest framework

# Greate our CL argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('explicit_test_names', metavar='test-name', type=str, nargs='*', help='Names of tests to run.')
args = parser.parse_args()

# Parse test registry
tests_yaml = yaml.load( file( "tests/tests.yaml") )

# Collect test names to run
run_these_tests = []
if len(args.explicit_test_names) > 0:
  # No duplicates
  run_these_tests = list(set(args.explicit_test_names))
  # Ensure that tests are registered
  for name in run_these_tests:
    if name not in tests_yaml['test_names']:
      raise Exception( "\"{0}\" is not a test registered in tests.yaml".format(name) )
else:
  run_these_tests = tests_yaml['test_names']

# Root and full import path for our modules
test_module_root = "tests.test_source"
test_module_names = map( lambda name: test_module_root + "." + name, run_these_tests )

# Collect all the modules
test_modules = map( lambda name: importlib.import_module( name ), test_module_names )

# Get all test classes that are defined only by our test files
# Process:
# 1. Get classes out of each module. Note: Also collects clases from imports in that module
# 2. Strip out classes that didnt come from our modules
# 3. Union them in a list
test_classes = reduce( lambda a,b: a+b, map( lambda test_module: filter( lambda class_: class_.__module__ in test_module_names , map( lambda a: a[1], inspect.getmembers( test_module, inspect.isclass ) ) ), test_modules ) )

# Create unittest suits from each test class
test_suits = map( lambda test_module: unittest.TestLoader().loadTestsFromTestCase( test_module ), test_classes )

# Run each test suit
for suit in test_suits:
  unittest.TextTestRunner().run(suit)
