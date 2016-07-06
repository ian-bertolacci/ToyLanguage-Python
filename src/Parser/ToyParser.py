from __future__ import print_function
from ply import yacc, lex
from AST.ToyStructure import *
from util import *

def get_parser( debug_mode = False):
  lexer = None
  parser = None

  if debug_mode:
    lexer = lex.lex( debug = True )
    parser = yacc.yacc( write_tables = True, debug = True )
  else:
    lexer = lex.lex( debug = False, errorlog = yacc.NullLogger() )
    parser = yacc.yacc( write_tables = False, debug = False, errorlog = yacc.NullLogger() )

  return parser

yacc.YaccProduction.__str__ = lambda self: "[" + (", ".join( str(self[i]) for i in xrange(len(self)) ) ) + "]"

tokens = [
          'PLUS','MINUS','EXP','TIMES','DIVIDE','MOD',
          'EQ','NEQ','LT','LTEQ','GT','GTEQ',
          'NOT','AND','OR',
          'LET', 'RETURN',
          'LPAREN','RPAREN', 'LSBRACE', 'RSBRACE', 'LCBRACE', 'RCBRACE',
          'ASSIGN', 'ARROW', 'COLON', 'SEMI', 'COMMA', 'DOT', 'DOTDOT',
          'INT','REAL',
          'STRING',
          'TRUE','FALSE',
          'ID']

'''
Order denotes the attempt precidence.
This is why t_TRUE and t_FALSE come before t_ID.
Otherwise It would tokenize both as IDs
'''

def t_error(t):
  raise Exception( "Illegal character while tokenizing: {0}".format( t.value[0]) )

def t_REAL(t):
  r'-?\d*\.\d+'
  t.value = Real_Literal( t.value, float(t.value) )
  return t

def t_INT(t):
  r'-?\d+'
  t.value = Int_Literal( t.value, int(t.value) )
  return t

def t_TRUE(t):
  r'true'
  t.value = Bool_Literal( t.value, True )
  return t

def t_FALSE(t):
  r'false'
  t.value = Bool_Literal( t.value, False )
  return t

def t_STRING(t):
  r'\".*\"'
  return t

def t_LET(t):
  r'let'
  return t

def t_RETURN(t):
  r'return'
  return t

def t_ASSIGN(t):
  r':='
  return t

def t_ARROW(t):
  r'->'
  return t

def t_DOT(t):
  r'\.'
  return t

def t_DOTDOT(t):
  r'\.\.'
  return t

def t_SEMI(t):
  r';'
  return t

def t_COLON(t):
  r':'
  return t

def t_COMMA(t):
  r','
  return t

def t_PLUS(t):
  r'\+'
  t.value = Operator_Token( '+' )
  return t

def t_MINUS(t):
  r'-'
  t.value = Operator_Token( '-' )
  return t

def t_EXP(t):
  r'\*\*'
  t.value = Operator_Token( '**' )
  return t

def t_TIMES(t):
  r'\*'
  t.value = Operator_Token( '*' )
  return t

def t_DIVIDE(t):
  r'/'
  t.value = Operator_Token( '/' )
  return t

def t_MOD(t):
  r'%'
  t.value = Operator_Token( '%' )
  return t

def t_NOT(t):
  r'not'
  t.value = Operator_Token( 'not' )
  return t

def t_AND(t):
  r'and'
  t.value = Operator_Token( 'and' )
  return t

def t_OR(t):
  r'or'
  t.value = Operator_Token( 'or' )
  return t

def t_EQ(t):
  r'=='
  t.value = Operator_Token( '==' )
  return t

def t_NEQ(t):
  r'!='
  t.value = Operator_Token( '!=' )
  return t

def t_LTEQ(t):
  r'<='
  t.value = Operator_Token( '<=' )
  return t

def t_LT(t):
  r'<'
  t.value = Operator_Token( '<' )
  return t

def t_GTEQ(t):
  r'>='
  t.value = Operator_Token( '>=' )
  return t

def t_GT(t):
  r'>'
  t.value = Operator_Token( '>' )
  return t

def t_LPAREN(t):
  r'\('
  t.value = Operator_Token( '(' )
  return t

def t_RPAREN(t):
  r'\)'
  t.value = Operator_Token( ')' )
  return t

def t_LSBRACE(t):
  r'\['
  t.value = Operator_Token( '[' )
  return t

def t_RSBRACE(t):
  r'\]'
  t.value = Operator_Token( ']' )
  return t

def t_LCBRACE(t):
  r'\{'
  t.value = Operator_Token( '{' )
  return t

def t_RCBRACE(t):
  r'\}'
  t.value = Operator_Token( '}' )
  return t

def t_ID(t):
  r'_*?[a-zA-Z][a-zA-Z0-9_]*'
  t.value = Identifier( str(t.value) )
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

t_ignore = " \t"

precedence = [
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MOD'),
    ('right','EXP'),
    ('left','EQ','NEQ','LT','LTEQ','GT','GTEQ'),
    ('left','AND','OR'),
    ('right','UMINUS','NOT')
    ]

start = 'program'

def p_error(p):
  raise Exception( "Illegal token while parsing: {0}".format(p) )

def p_program(p):
  '''program : statement_list'''
  p[0] = p[1]

def p_statement_list(p):
  '''statement_list : statement_list_base
                    | statement_list_recursive'''
  p[0] = p[1]

def p_statement_list_base(p):
  '''statement_list_base : statement'''
  p[0] = [ p[1] ]

def p_statement_list_recursive(p):
  '''statement_list_recursive : statement_list_base statement_list'''
  p[0] = p[1] + p[2]

def p_statement(p):
  '''statement : let_decl
               | return_stmt
               | statement_block'''
  p[0] = p[1]

def p_statment_block(p):
  '''statement_block : LCBRACE statement_list RCBRACE'''
  p[0] = p[2]

def p_return_stmt(p):
  '''return_stmt : RETURN exp SEMI'''
  p[0] = Return_Statement( value = p[2] )

def p_let_decl(p):
  '''let_decl : let_decl_no_assign
              | let_decl_assign'''
  p[0] = p[1]

def p_let_decl_no_assign(p):
  '''let_decl_no_assign : LET typed_id SEMI'''
  p[0] = Let_Declaration_Node( typed_id=p[2], init=None )

def p_let_decl_assign(p):
  '''let_decl_assign : LET typed_id ASSIGN exp SEMI'''
  p[0] = Let_Declaration_Node( typed_id=p[2], init=p[4] )

def p_type_decl(p):
  '''type_decl : ID
               | closure_type_decl
               | wrapped_type_list'''
  p[0] = p[1]

def p_closure_type_decl(p):
  '''closure_type_decl : LPAREN type_list ARROW type_decl RPAREN'''
  p[0] = Closure_Type( in_types=p[2], out_type=p[4] )

def p_wrapped_type_list(p):
  '''wrapped_type_list : wrapped_type_list_base
                       | wrapped_type_list_tail'''
  p[0] = p[1]

def p_wrapped_type_list_base(p):
  '''wrapped_type_list_base : LPAREN type_decl COMMA RPAREN'''
  p[0] = Type_List( [ p[2] ] )

def p_wrapped_type_list_tail(p):
  '''wrapped_type_list_tail : LPAREN type_decl COMMA type_list RPAREN'''
  p[4].prepend( p[2] )
  p[0] = p[4]

def p_type_list(p):
  '''type_list : type_list_base
               | type_list_recursive'''
  p[0] = p[1]

def p_type_list_base(p):
  '''type_list_base : type_decl'''
  p[0] = Type_List( [ p[1] ] )

def p_type_list_recursive(p):
  '''type_list_recursive : type_decl COMMA type_list'''
  p[3].prepend( p[1] )
  p[0] = p[3]

def p_typed_id(p):
  '''typed_id : ID COLON type_decl'''
  p[0] = Typed_Id( id=p[1], id_type=p[3] )

def p_typed_id_list(p):
  '''typed_id_list : typed_id_list_base
                   | typed_id_list_recursive'''
  p[0] = p[1]

def p_typed_id_list_base(p):
  '''typed_id_list_base : typed_id'''
  p[0] = Typed_Id_List( [ p[1] ] )

def p_typed_id_list_recursive(p):
  '''typed_id_list_recursive : typed_id COMMA typed_id_list'''
  p[3].prepend( p[1] )
  p[0] = p[3]

def p_exp(p):
  '''exp : value
         | bin_op_exp
         | un_op_exp
         | paren_exp
         | closure'''
  p[0] = p[1]

def p_closure(p):
  '''closure : closure_param_decl statement_block'''
  p[0] = Closure_Node( closure_type=p[1], body=p[2] )

def p_closure_param_decl(p):
  '''closure_param_decl : LPAREN typed_id_list ARROW type_decl RPAREN'''
  p[0] = Closure_Param( in_params = p[2], out_type = p[4] )

def p_bin_op_exp(p):
  '''bin_op_exp : exp PLUS exp
                | exp MINUS exp
                | exp TIMES exp
                | exp MOD exp
                | exp DIVIDE exp
                | exp EXP exp
                | exp EQ exp
                | exp NEQ exp
                | exp LT exp
                | exp LTEQ exp
                | exp GT exp
                | exp GTEQ exp
                | exp AND exp
                | exp OR exp'''
  p[0] = Binary_Operator_Node( op=p[2], lhs=p[1], rhs=p[3] )
  #debug_print( "Binary op exp:", p[0] )

def p_paren(p):
  '''paren_exp : LPAREN exp RPAREN'''
  p[0] = p[2]

def p_un_op_exp(p):
  '''un_op_exp : NOT exp
               | MINUS exp %prec UMINUS'''
  p[0] = Unary_Operator_Node( op=p[1], exp=p[2] )
  #debug_print( "Unary op exp:", p[0])

def p_value(p):
  '''value : INT
           | REAL
           | TRUE
           | FALSE
           | STRING
           | ID'''
  p[0] = p[1]
  #debug_print( "Value:", p[0] )
