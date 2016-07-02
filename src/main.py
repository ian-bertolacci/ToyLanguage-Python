from __future__ import print_function

import parser
import util
from parser import *
from TypePass import TypePass
from PrintPass import *
from util import *
from unit_test_parser import parse_tests

util.DEBUG_PRINT = False

if __name__ == "__main__":
  lex.lex()
  parser = yacc.yacc()
  for test in parse_tests:
    tree = parser.parse(test)
    print( PrintPass( tree ).run_pass() )
    print( TypePass(tree).run_pass() )
