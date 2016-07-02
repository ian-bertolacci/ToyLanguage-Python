from __future__ import print_function
from AST.ToyStructure import *
from Pass import *

class PrintPass(Pass):

  def __init__( self, tree ):
    self.root = tree;

  def run_pass( self ):
    return self.root.accept( self )

  # Binary Operator node
  def visit_Binary_Operator(self,node):
    return \
      " ".join(
                [
                self.enter_Binary_Operator(node),
                self.visit_Binary_Operator_LHS(node),
                str(node.op.op),
                self.visit_Binary_Operator_RHS(node),
                self.exit_Binary_Operator(node),
                ]
              )

  def enter_Binary_Operator(self,node):
    return "("

  def exit_Binary_Operator(self,node):
      return ")"

  def visit_Binary_Operator_LHS(self,node):
    return node.lhs.accept( self )

  def visit_Binary_Operator_RHS(self,node):
    return node.rhs.accept( self )

  # Unary Operator Node
  def visit_Unary_Operator(self,node):
    return \
      " ".join(
                [
                self.enter_Unary_Operator(node),
                str(node.op.op),
                self.visit_Unary_Operator_expression(node),
                self.exit_Unary_Operator(node),
                ]
              )

  def enter_Unary_Operator(self,node):
    return "("

  def exit_Unary_Operator(self,node):
      return ")"

  def visit_Unary_Operator_expression(self,node):
    return node.exp.accept( self )

  # Identifier Node
  def visit_Identifier(self, node):
    return str( node.symbol )

  # Real literal
  def visit_Real_Literal(self, node):
    return str(node.value)

  # Int literal
  def visit_Int_Literal(self, node):
    return str(node.value)

  # Bool literal
  def visit_Bool_Literal(self, node):
    return str(node.value)
