from __future__ import print_function
from AST.ToyStructure import *

class Pass:

  # Binary Operator node
  def visit_Binary_Operator(self,node):
    self.enter_Binary_Operator(node)
    self.visit_Binary_Operator_LHS(node)
    self.visit_Binary_Operator_RHS(node)
    self.exit_Binary_Operator(node)

  def enter_Binary_Operator(self,node):
    pass

  def visit_Binary_Operator_LHS(self,node):
    node.lhs.accept( self )

  def visit_Binary_Operator_RHS(self,node):
    node.rhs.accept( self )

  def exit_Binary_Operator(self,node):
    pass

  # Unary Operator Node
  def visit_Unary_Operator(self,node):
    self.enter_Unary_Operator(node)
    self.visit_Unary_Operator_expression(node)
    self.exit_Unary_Operator(node)

  def enter_Unary_Operator(self,node):
    pass

  def visit_Unary_Operator_expression(self,node):
    node.exp.accept( self )

  def exit_Unary_Operator(self,node):
    pass

  # Identifier Node
  def visit_Identifier(self, node):
    self.enter_Identifier(node)
    self.exit_Identifier(node)

  def enter_Identifier(self, node):
    pass

  def exit_Identifier(self, node):
    pass

  # Real literal
  def visit_Real_Literal(self, node):
    self.enter_Real_Literal(node)
    self.exit_Real_Literal(node)

  def enter_Real_Literal(self, node):
    pass

  def exit_Real_Literal(self, node):
    pass

  # Int literal
  def visit_Int_Literal(self, node):
    self.enter_Int_Literal(node)
    self.exit_Int_Literal(node)

  def enter_Int_Literal(self, node):
    pass

  def exit_Int_Literal(self, node):
    pass

  # Bool literal
  def visit_Bool_Literal(self, node):
    self.enter_Bool_Literal(node)
    self.exit_Bool_Literal(node)

  def enter_Bool_Literal(self, node):
    pass

  def exit_Bool_Literal(self, node):
    pass
