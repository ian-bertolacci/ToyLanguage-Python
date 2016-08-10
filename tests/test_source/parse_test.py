from __future__ import print_function
import unittest
from Parser.ToyParser import *
from AST.ToyStructure import *
import util

debug_mode = False

class ParseTests(unittest.TestCase):

  def do_tests(self, start_production, tests, is_test = True, print_tree = False ):
    lexer = None
    parser = None
    if debug_mode:
      lexer = lex.lex( debug = True )
      parser = yacc.yacc( start = start_production, debug = True, write_tables = False )
    else:
      lexer = lex.lex( debug = False, errorlog = yacc.NullLogger() )
      parser = yacc.yacc( start = start_production, write_tables = False, debug = False, errorlog = yacc.NullLogger() )


    if print_tree:
      print( "\n" )

    for test in tests:
      s = parser.parse(test[0], lexer = lexer)
      if print_tree:
        print( "[\"{0}\", {1}],".format(test[0], s) )
      if is_test:
        self.assertEqual( s, test[1] )


  def test_INT_lex(self):
    start_production = "value"
    tests = [
              ["0", Int_Literal(text='0', value=0) ],
              ["1", Int_Literal(text='1', value=1) ],
              ["1234567890", Int_Literal(text='1234567890', value=1234567890) ],
              ["-1", Int_Literal(text='-1', value=-1) ],
              ["-1234567890", Int_Literal(text='-1234567890', value=-1234567890) ],
            ]

    self.do_tests( start_production, tests )


  def test_REAL_lex(self):
    start_production = "value"
    tests = [
              ["1.5", Real_Literal(text='1.5', value=1.5) ],
              [".5", Real_Literal(text='.5', value=0.5) ],
              ["-1.5", Real_Literal(text='-1.5', value=-1.5) ],
              ["-.5", Real_Literal(text='-.5', value=-0.5) ],
            ]

    self.do_tests( start_production, tests )


  def test_BOOLE_lex(self):
    start_production = "value"
    tests = [
              ["true", Bool_Literal(text='true', value=True) ],
              ["false", Bool_Literal(text='false', value=False) ],
            ]

    self.do_tests( start_production, tests )


  def test_ID_lex(self):
    start_production = "value"
    tests = [
              ["a", Identifier(symbol='a') ],
              ["_a", Identifier(symbol='_a') ],
              ["_a_", Identifier(symbol='_a_') ],
              ["__a__", Identifier(symbol='__a__') ],
              ["ab", Identifier(symbol='ab') ],
              ["_ab", Identifier(symbol='_ab') ],
              ["_ab_", Identifier(symbol='_ab_') ],
              ["__ab__", Identifier(symbol='__ab__') ],
            ]

    self.do_tests( start_production, tests )


  def test_arithmetic_parse(self):
    start_production = "expression"
    tests = [
              ["1 + 2", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 - 2", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 * 2", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 / 2", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 % 2", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 ** 2", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 + 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 * 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 / 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 / 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 % 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 % 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 ** 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 ** 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 + 2 * 3 + 4", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))), rhs=Int_Literal(text='4', value=4)) ],
              ["1 + 2 / 3 + 4", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))), rhs=Int_Literal(text='4', value=4)) ],
              ["1 + 2 % 3 + 4", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))), rhs=Int_Literal(text='4', value=4)) ],
              ["1 + 2 ** 3 + 4", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))), rhs=Int_Literal(text='4', value=4)) ],
              ["1 + 2 * (3 + 4)", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='2', value=2), rhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='3', value=3), rhs=Int_Literal(text='4', value=4)))) ],
              ["1 + 2 / (3 + 4)", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='2', value=2), rhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='3', value=3), rhs=Int_Literal(text='4', value=4)))) ],
              ["1 + 2 % (3 + 4)", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='2', value=2), rhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='3', value=3), rhs=Int_Literal(text='4', value=4)))) ],
              ["1 + 2 ** (3 + 4)", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='2', value=2), rhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='3', value=3), rhs=Int_Literal(text='4', value=4)))) ],
              ["-1 + 2 / a ** (1.3 + -0.1)", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='-1', value=-1), rhs=Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='2', value=2), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Identifier(symbol='a'), rhs=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Real_Literal(text='1.3', value=1.3), rhs=Real_Literal(text='-0.1', value=-0.1))))) ],
            ]

    self.do_tests( start_production, tests )


  def test_comparison_parse(self):
    start_production = "expression"
    tests = [
              ["1", Int_Literal(text='1', value=1) ],
              ["1 == 2", Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 != 2", Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 < 2", Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 <= 2", Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 > 2", Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 >= 2", Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)) ],
              ["1 + 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 == 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 != 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 < 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 <= 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 > 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 + 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 - 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 * 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 / 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 % 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 ** 2 >= 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3))) ],
              ["1 == 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 == 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 == 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 == 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 == 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 == 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='=='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 != 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='!='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 < 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 <= 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 > 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>'), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 + 3", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 - 3", Binary_Operator_Expression(op=Operator_Token(op='-'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 * 3", Binary_Operator_Expression(op=Operator_Token(op='*'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 / 3", Binary_Operator_Expression(op=Operator_Token(op='/'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 % 3", Binary_Operator_Expression(op=Operator_Token(op='%'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
              ["1 >= 2 ** 3", Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='>='), lhs=Int_Literal(text='1', value=1), rhs=Int_Literal(text='2', value=2)), rhs=Int_Literal(text='3', value=3)) ],
            ]

    self.do_tests( start_production, tests )


  def test_boolean_parse(self):
    start_production = "expression"
    tests = [
              ["true", Bool_Literal(text='true', value=True) ],
              ["false", Bool_Literal(text='false', value=False) ],
              ["true and false", Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False)) ],
              ["true or false", Binary_Operator_Expression(op=Operator_Token(op='or'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False)) ],
              ["not true", Unary_Operator_Expression(op=Operator_Token(op='not'), expression=Bool_Literal(text='true', value=True)) ],
              ["true and false or true", Binary_Operator_Expression(op=Operator_Token(op='or'), lhs=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False)), rhs=Bool_Literal(text='true', value=True)) ],
              ["true or false and true", Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Binary_Operator_Expression(op=Operator_Token(op='or'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False)), rhs=Bool_Literal(text='true', value=True)) ],
              ["(true and false) or true", Binary_Operator_Expression(op=Operator_Token(op='or'), lhs=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False)), rhs=Bool_Literal(text='true', value=True)) ],
              ["true and (false or true)", Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Binary_Operator_Expression(op=Operator_Token(op='or'), lhs=Bool_Literal(text='false', value=False), rhs=Bool_Literal(text='true', value=True))) ],
              ["not (true and false)", Unary_Operator_Expression(op=Operator_Token(op='not'), expression=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Bool_Literal(text='false', value=False))) ],
              ["not true and false", Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Unary_Operator_Expression(op=Operator_Token(op='not'), expression=Bool_Literal(text='true', value=True)), rhs=Bool_Literal(text='false', value=False)) ],
            ]

    self.do_tests( start_production, tests )


  def test_mixed_expression_lex(self):
    start_production = "expression"
    tests = [
              ["1 < 2 and true", Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Int_Literal(text='2', value=2), rhs=Bool_Literal(text='true', value=True))) ],
              ["true and 1 < 2", Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Bool_Literal(text='true', value=True), rhs=Int_Literal(text='1', value=1)), rhs=Int_Literal(text='2', value=2)) ],
              ["1 + 2 < 3 ** 4 and not false", Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Int_Literal(text='1', value=1), rhs=Binary_Operator_Expression(op=Operator_Token(op='**'), lhs=Binary_Operator_Expression(op=Operator_Token(op='<'), lhs=Int_Literal(text='2', value=2), rhs=Int_Literal(text='3', value=3)), rhs=Binary_Operator_Expression(op=Operator_Token(op='and'), lhs=Int_Literal(text='4', value=4), rhs=Unary_Operator_Expression(op=Operator_Token(op='not'), expression=Bool_Literal(text='false', value=False))))) ],
            ]

    self.do_tests( start_production, tests )

  def test_type_declaration_parse(self):
    start_production="type_declaration"
    tests = [
      ["a", Identifier(symbol='a')],
      ["(a,)", Type_List(types=[Identifier(symbol='a')])],
      ["(a,b)", Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')])],
      ["(a,b,c)", Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Identifier(symbol='c')])],
      ["(a,(b,))", Type_List(types=[Identifier(symbol='a'), Type_List(types=[Identifier(symbol='b')])])],
      ["(a,(b,c))", Type_List(types=[Identifier(symbol='a'), Type_List(types=[Identifier(symbol='b'), Identifier(symbol='c')])])],
      ["((a,),b,c)", Type_List(types=[Type_List(types=[Identifier(symbol='a')]), Identifier(symbol='b'), Identifier(symbol='c')])],
      ["((a,b),c,d)", Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), Identifier(symbol='c'), Identifier(symbol='d')])],
      ["((a,b),(c,))", Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), Type_List(types=[Identifier(symbol='c')])])],
      ["((a,b),(c,d))", Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')])])],
      ["((a,b),(c,(d,)))", Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), Type_List(types=[Identifier(symbol='c'), Type_List(types=[Identifier(symbol='d')])])])],
      ["((a,b),(c,(d,e)))", Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), Type_List(types=[Identifier(symbol='c'), Type_List(types=[Identifier(symbol='d'), Identifier(symbol='e')])])])],
    ]

    self.do_tests( start_production, tests )

  def test_closure_type_declaration_parse(self):
    start_production="closure_type_declaration"
    tests = [
      ["(a->b)", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Identifier(symbol='b'))],
      ["(a->(b,))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Type_List(types=[Identifier(symbol='b')]))],
      ["(a->(b,c))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Type_List(types=[Identifier(symbol='b'), Identifier(symbol='c')]))],
      ["(a->(b,c,(d,e)))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Type_List(types=[Identifier(symbol='b'), Identifier(symbol='c'), Type_List(types=[Identifier(symbol='d'), Identifier(symbol='e')])]))],

      ["(a,b->c)", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Identifier(symbol='c'))],
      ["(a,b->(c,))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Type_List(types=[Identifier(symbol='c')]))],
      ["(a,b->(c,d))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')]))],
      ["(a,b->(c,d,(e,f)))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d'), Type_List(types=[Identifier(symbol='e'), Identifier(symbol='f')])]))],

      ["(a,b,c->d)", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Identifier(symbol='c')]), out_type=Identifier(symbol='d'))],
      ["(a,b,c->(d,))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Identifier(symbol='c')]), out_type=Type_List(types=[Identifier(symbol='d')]))],
      ["(a,b,c->(d,e))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Identifier(symbol='c')]), out_type=Type_List(types=[Identifier(symbol='d'), Identifier(symbol='e')]))],
      ["(a,b,c->(d,e,(f,g)))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Identifier(symbol='c')]), out_type=Type_List(types=[Identifier(symbol='d'), Identifier(symbol='e'), Type_List(types=[Identifier(symbol='f'), Identifier(symbol='g')])]))],

      ["((a,)->b)", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a')])]), out_type=Identifier(symbol='b'))],
      ["((a,)->(b,))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a')])]), out_type=Type_List(types=[Identifier(symbol='b')]))],
      ["((a,)->(b,c))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a')])]), out_type=Type_List(types=[Identifier(symbol='b'), Identifier(symbol='c')]))],
      ["((a,)->(b,c,(d,e)))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a')])]), out_type=Type_List(types=[Identifier(symbol='b'), Identifier(symbol='c'), Type_List(types=[Identifier(symbol='d'), Identifier(symbol='e')])]))],

      ["((a,b)->c)", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')])]), out_type=Identifier(symbol='c'))],
      ["((a,b)->(c,))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')])]), out_type=Type_List(types=[Identifier(symbol='c')]))],
      ["((a,b)->(c,d))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')])]), out_type=Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')]))],
      ["((a,b)->(c,d,(e,f)))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')])]), out_type=Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d'), Type_List(types=[Identifier(symbol='e'), Identifier(symbol='f')])]))],

      ["((a,b,(c,d))->e)", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')])])]), out_type=Identifier(symbol='e'))],
      ["((a,b,(c,d))->(e,))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')])])]), out_type=Type_List(types=[Identifier(symbol='e')]))],
      ["((a,b,(c,d))->(e,f))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')])])]), out_type=Type_List(types=[Identifier(symbol='e'), Identifier(symbol='f')]))],
      ["((a,b,(c,d))->(e,f,(g,h)))", Closure_Type(in_types=Type_List(types=[Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b'), Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')])])]), out_type=Type_List(types=[Identifier(symbol='e'), Identifier(symbol='f'), Type_List(types=[Identifier(symbol='g'), Identifier(symbol='h')])]))],

      ["(a->(c->b))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='c')]), out_type=Identifier(symbol='b')))],
      ["(a->(c->(b->d)))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a')]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='c')]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='b')]), out_type=Identifier(symbol='d'))))],
      ["(a,b->(c->d))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='c')]), out_type=Identifier(symbol='d')))],
      ["(a,b->(c,d->e))", Closure_Type(in_types=Type_List(types=[Identifier(symbol='a'), Identifier(symbol='b')]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='c'), Identifier(symbol='d')]), out_type=Identifier(symbol='e')))],
    ]

    self.do_tests( start_production, tests )

  def test_closure_parameter_declaration_parse(self):
    start_production="closure_parameter_declaration"
    tests = [
      ["( a : type_a -> type_b )", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a'))]), out_type=Identifier(symbol='type_b'))],
      ["( a : type_a, b : type_b -> type_c )", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a')), Typed_Id(id=Identifier(symbol='b'), id_type=Identifier(symbol='type_b'))]), out_type=Identifier(symbol='type_c'))],
      ["( a : (type_a,) -> type_b )", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Type_List(types=[Identifier(symbol='type_a')]))]), out_type=Identifier(symbol='type_b'))],
      ["( a : (type_a, type_b) -> type_c )", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Type_List(types=[Identifier(symbol='type_a'), Identifier(symbol='type_b')]))]), out_type=Identifier(symbol='type_c'))],
      ["( a : (type_a, type_b), c : (type_c, type_d) -> type_e )", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Type_List(types=[Identifier(symbol='type_a'), Identifier(symbol='type_b')])), Typed_Id(id=Identifier(symbol='c'), id_type=Type_List(types=[Identifier(symbol='type_c'), Identifier(symbol='type_d')]))]), out_type=Identifier(symbol='type_e'))],
      ["( a : type_a -> (type_b -> type_c))", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a'))]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='type_b')]), out_type=Identifier(symbol='type_c')))],
      ["( a : type_a -> (type_b, type_c -> type_d))", Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a'))]), out_type=Closure_Type(in_types=Type_List(types=[Identifier(symbol='type_b'), Identifier(symbol='type_c')]), out_type=Identifier(symbol='type_d')))],
    ]

    self.do_tests( start_production, tests )

  def test_closure_parse(self):
    start_production="closure"
    tests = [
      ["( a : type_a -> type_a ){ return a; }", Closure(closure_type=Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a'))]), out_type=Identifier(symbol='type_a')), body=[Return_Statement(value=Identifier(symbol='a'))])],
      ["( a : type_a -> type_a ){ let b : type_a := -a; return b; }", Closure(closure_type=Closure_Parameter_Declaration(in_params=Typed_Id_List(typed_ids=[Typed_Id(id=Identifier(symbol='a'), id_type=Identifier(symbol='type_a'))]), out_type=Identifier(symbol='type_a')), body=[Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='b'), id_type=Identifier(symbol='type_a')), init=Unary_Operator_Expression(op=Operator_Token(op='-'), expression=Identifier(symbol='a'))), Return_Statement(value=Identifier(symbol='b'))])],
    ]

    self.do_tests( start_production, tests )

  def test_let_statement_parse(self):
    start_production="statement"
    tests = [
      ["let x : a;", Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='x'), id_type=Identifier(symbol='a')), init=None)],
      ["let x : (a,);", Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='x'), id_type=Type_List(types=[Identifier(symbol='a')])), init=None)],
      ["let x : a;", Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='x'), id_type=Identifier(symbol='a')), init=None)],
      ["let x : a;", Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='x'), id_type=Identifier(symbol='a')), init=None)],

      ["let x : int := 10;", Let_Declaration(typed_id=Typed_Id(id=Identifier(symbol='x'), id_type=Identifier(symbol='int')), init=Int_Literal(text='10', value=10))]
    ]

    self.do_tests( start_production, tests )

  def test_closure_evaluation_parse(self):
    start_production = "expression"
    tests = [
      ["func1()", Closure_Evaluation(closure_expression=Identifier(symbol='func1'), parameters=[])],
      ["func2( a )", Closure_Evaluation(closure_expression=Identifier(symbol='func2'), parameters=[Unnamed_Parameter(value=Identifier(symbol='a'))])],
      ["func3( param := a )", Closure_Evaluation(closure_expression=Identifier(symbol='func3'), parameters=[Named_Parameter(id=Identifier(symbol='param'), value=Identifier(symbol='a'))])],
      ["func4( param := a + b )", Closure_Evaluation(closure_expression=Identifier(symbol='func4'), parameters=[Named_Parameter(id=Identifier(symbol='param'), value=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Identifier(symbol='a'), rhs=Identifier(symbol='b')))])],
      ["func5( a, b )", Closure_Evaluation(closure_expression=Identifier(symbol='func5'), parameters=[Unnamed_Parameter(value=Identifier(symbol='a')), Unnamed_Parameter(value=Identifier(symbol='b'))])],
      ["func6( param := a, b )", Closure_Evaluation(closure_expression=Identifier(symbol='func6'), parameters=[Named_Parameter(id=Identifier(symbol='param'), value=Identifier(symbol='a')), Unnamed_Parameter(value=Identifier(symbol='b'))])],
      ["func6( a, param := b )", Closure_Evaluation(closure_expression=Identifier(symbol='func6'), parameters=[Unnamed_Parameter(value=Identifier(symbol='a')), Named_Parameter(id=Identifier(symbol='param'), value=Identifier(symbol='b'))])],
      ["func7( param := a + b, c )", Closure_Evaluation(closure_expression=Identifier(symbol='func7'), parameters=[Named_Parameter(id=Identifier(symbol='param'), value=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Identifier(symbol='a'), rhs=Identifier(symbol='b'))), Unnamed_Parameter(value=Identifier(symbol='c'))])],
      ["func8( a, param := b + c )", Closure_Evaluation(closure_expression=Identifier(symbol='func8'), parameters=[Unnamed_Parameter(value=Identifier(symbol='a')), Named_Parameter(id=Identifier(symbol='param'), value=Binary_Operator_Expression(op=Operator_Token(op='+'), lhs=Identifier(symbol='b'), rhs=Identifier(symbol='c')))])],
      ["func9( func10() )", Closure_Evaluation(closure_expression=Identifier(symbol='func9'), parameters=[Unnamed_Parameter(value=Closure_Evaluation(closure_expression=Identifier(symbol='func10'), parameters=[]))])],
      ["func11( func12() )()", Closure_Evaluation(closure_expression=Closure_Evaluation(closure_expression=Identifier(symbol='func11'), parameters=[Unnamed_Parameter(value=Closure_Evaluation(closure_expression=Identifier(symbol='func12'), parameters=[]))]), parameters=[])],
    ]

    self.do_tests( start_production, tests )

if __name__ == "__main__":
  pass
