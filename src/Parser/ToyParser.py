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

# Lexer states
states = [
  ('comment','exclusive'),
]

tokens = [
          'PLUS','MINUS','EXP','TIMES','DIVIDE','MOD',
          'EQ','NEQ','LT','LTEQ','GT','GTEQ',
          'NOT','AND','OR',
          'LET', 'RETURN', 'IF', 'THEN', 'ELSE',
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

def t_LINE_COMMENT(t):
  r'//.*\n'

def t_COMMENT_BLOCK(t):
  r'/\*'
  t.lexer.comment_start = t.lexer.lexpos
  t.lexer.comment_depth = 1
  t.lexer.begin('comment')

def t_comment_OPEN_COMMENT(t):
 r'/\*'
 t.lexer.comment_depth += 1

def t_comment_CLOSE_COMMENT(t):
  r'\*/'
  t.lexer.comment_depth -= 1
  if t.lexer.comment_depth < 1:
    t.value = t.lexer.lexdata[t.lexer.comment_start:t.lexer.lexpos-2]
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')

def t_comment_error(t):
  t.lexer.skip(1)

t_comment_ignore = " \t\n"

def t_IF(t):
  r'if'
  return t

def t_THEN(t):
  r'then'
  return t

def t_ELSE(t):
  r'else'
  return t

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
    ('right','UMINUS','NOT'),
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
  '''statement : let_declaration
               | return_statement
               | statement_block
               | expression_statement
               | conditional_statement'''
  p[0] = p[1]

def p_statement_block(p):
  '''statement_block : LCBRACE statement_list RCBRACE'''
  p[0] = p[2]

def p_return_statement(p):
  '''return_statement : RETURN expression SEMI'''
  p[0] = Return_Statement( value = p[2] )

def p_conditional_statement(p):
  '''conditional_statement : basic_if
                           | if_else'''
  p[0] = p[1]

def p_basic_if(p):
  '''basic_if : IF LPAREN expression RPAREN statement_block'''
  p[0] = If_Statement( condition = p[3], then_body = p[5], else_body = [] )

def p_if_else(p):
  '''if_else : basic_if ELSE statement_block
             | basic_if ELSE basic_if
             | basic_if ELSE if_else'''
  p[0] = If_Statement( condition = p[1].condition, then_body = p[1].then_body, else_body = p[3] )

def p_let_declaration(p):
  '''let_declaration : let_declaration_no_assign
                     | let_declaration_assign'''
  p[0] = p[1]

def p_let_declaration_no_assign(p):
  '''let_declaration_no_assign : LET typed_id SEMI'''
  p[0] = Let_Declaration( typed_id=p[2], init=None )

def p_let_declaration_assign(p):
  '''let_declaration_assign : LET typed_id ASSIGN expression SEMI'''
  p[0] = Let_Declaration( typed_id=p[2], init=p[4] )

def p_type_declaration(p):
  '''type_declaration : ID
                      | closure_type_declaration
                      | wrapped_type_list'''
  p[0] = p[1]

def p_closure_type_declaration(p):
  '''closure_type_declaration : LPAREN type_list ARROW type_declaration RPAREN'''
  p[0] = Closure_Type( in_types=p[2], out_type=p[4] )

def p_wrapped_type_list(p):
  '''wrapped_type_list : wrapped_type_list_base
                       | wrapped_type_list_tail'''
  p[0] = p[1]

def p_wrapped_type_list_base(p):
  '''wrapped_type_list_base : LPAREN type_declaration COMMA RPAREN'''
  p[0] = Type_List( [ p[2] ] )

def p_wrapped_type_list_tail(p):
  '''wrapped_type_list_tail : LPAREN type_declaration COMMA type_list RPAREN'''
  p[4].prepend( p[2] )
  p[0] = p[4]

def p_type_list(p):
  '''type_list : type_list_base
               | type_list_recursive'''
  p[0] = p[1]

def p_type_list_base(p):
  '''type_list_base : type_declaration'''
  p[0] = Type_List( [ p[1] ] )

def p_type_list_recursive(p):
  '''type_list_recursive : type_declaration COMMA type_list'''
  p[3].prepend( p[1] )
  p[0] = p[3]

def p_typed_id(p):
  '''typed_id : ID COLON type_declaration'''
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

def p_expression_statement(p):
  '''expression_statement : expression SEMI'''
  p[0] = p[1]

def p_expression(p):
  '''expression : binary_operator_expression
                | unary_operator_expression
                | closed_expression
                | conditional_expression'''
  p[0] = p[1]

def p_closed_expression(p):
  '''closed_expression : value
                       | parenthesized_expression
                       | closure
                       | closure_evaluation_expression'''
  p[0] = p[1]

def p_conditional_expression(p):
  '''conditional_expression : IF LPAREN expression RPAREN THEN expression ELSE expression'''
  p[0] = Conditional_Exp( condition = p[3], then_body = p[6], else_body = p[8] )

def p_closure_evaluation_expression(p):
  '''closure_evaluation_expression : closed_expression parameter_evaluation_list'''
  p[0] = Closure_Evaluation( closure_expression=p[1], parameters=p[2] )

def p_parameter_evaluation_list(p):
  '''parameter_evaluation_list : parameter_evaluation_list_empty
                               | parameter_evaluation_list_non_empty'''
  p[0] = p[1]

def p_parameter_evaluation_list_empty(p):
  '''parameter_evaluation_list_empty : LPAREN RPAREN'''
  p[0] = []

def p_parameter_evaluation_list_non_empty(p):
  '''parameter_evaluation_list_non_empty : LPAREN parameter_evaluation_list_unwrapped RPAREN'''
  p[0] = p[2]

def p_parameter_evaluation_list_unwrapped(p):
  '''parameter_evaluation_list_unwrapped : parameter_evaluation_list_unwrapped_base
                                         | parameter_evaluation_list_unwrapped_recursive'''
  p[0] = p[1]

def p_parameter_evaluation_list_unwrapped_base(p):
  '''parameter_evaluation_list_unwrapped_base : parameter_evaluation_list_unwrapped_base_unnamed
                                              | parameter_evaluation_list_unwrapped_base_named'''
  p[0] = [ p[1] ]

def p_parameter_evaluation_list_unwrapped_base_unnamed(p):
  '''parameter_evaluation_list_unwrapped_base_unnamed : expression'''
  p[0] = Unnamed_Parameter( value = p[1] )

def p_parameter_evaluation_list_unwrapped_base_named(p):
  '''parameter_evaluation_list_unwrapped_base_named : ID ASSIGN expression'''
  p[0] = Named_Parameter( id = p[1], value = p[3] )

def p_parameter_evaluation_list_unwrapped_recursive(p):
  '''parameter_evaluation_list_unwrapped_recursive : parameter_evaluation_list_unwrapped_base COMMA parameter_evaluation_list_unwrapped'''
  p[0] = p[1] + p[3]

def p_closure(p):
  '''closure : closure_parameter_declaration statement_block'''
  p[0] = Closure( closure_type=p[1], body=p[2] )

def p_closure_parameter_declaration(p):
  '''closure_parameter_declaration : LPAREN typed_id_list ARROW type_declaration RPAREN'''
  p[0] = Closure_Parameter_Declaration( in_params = p[2], out_type = p[4] )

def p_binary_operator_expression(p):
  '''binary_operator_expression : expression PLUS expression
                                | expression MINUS expression
                                | expression TIMES expression
                                | expression MOD expression
                                | expression DIVIDE expression
                                | expression EXP expression
                                | expression EQ expression
                                | expression NEQ expression
                                | expression LT expression
                                | expression LTEQ expression
                                | expression GT expression
                                | expression GTEQ expression
                                | expression AND expression
                                | expression OR expression'''
  p[0] = Binary_Operator_Expression( op=p[2], lhs=p[1], rhs=p[3] )

def p_parenthesized_expression(p):
  '''parenthesized_expression : LPAREN expression RPAREN'''
  p[0] = p[2]

def p_unary_operator_expression(p):
  '''unary_operator_expression : NOT expression
                               | MINUS expression %prec UMINUS'''
  p[0] = Unary_Operator_Expression( op=p[1], expression=p[2] )

def p_value(p):
  '''value : INT
           | REAL
           | TRUE
           | FALSE
           | STRING
           | ID'''
  p[0] = p[1]
