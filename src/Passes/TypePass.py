from __future__ import print_function
from AST.ToyStructure import *
from Pass import Pass

class TypePass(Pass):
  def __init__( self, tree ):
    self.root = tree;

  def run_pass( self ):
    return self.root.accept( self )

  # Binary Operator node
  def visit_Binary_Operator(self,node):
    left_t = self.visit_Binary_Operator_LHS(node)
    right_t = self.visit_Binary_Operator_RHS(node)

  def visit_Binary_Operator_LHS(self,node):
    return node.lhs.accept( self )

  def visit_Binary_Operator_RHS(self,node):
    return node.rhs.accept( self )

  # Unary Operator Node
  def visit_Unary_Operator(self,node):
    return self.visit_Unary_Operator_expression(node)

  def visit_Unary_Operator_expression(self,node):
    return node.exp.accept( self )

  # Identifier Node
  def visit_Identifier(self, node):
    self.enter_Identifier(node)
    self.exit_Identifier(node)

  # Real literal
  def visit_Real_Literal(self, node):
    return 'REAL'

  # Int literal
  def visit_Int_Literal(self, node):
    return 'INT'

  # Bool literal
  def visit_Bool_Literal(self, node):
    return 'BOOL'
