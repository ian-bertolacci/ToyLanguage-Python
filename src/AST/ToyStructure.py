from __future__ import print_function
from collections import namedtuple

# Tokens / Leaf Nodes
Operator_Token = namedtuple( "Operator_Token", ['op'] )

Bool_Literal = namedtuple( "Bool_Literal", ['text','value'] )
Bool_Literal.accept = lambda _self,visitor: visitor.visit_Bool_Literal(_self)

Int_Literal = namedtuple( "Int_Literal", ['text','value'] )
Int_Literal.accept = lambda _self,visitor: visitor.visit_Int_Literal(_self)

Real_Literal = namedtuple( "Real_Literal", ['text','value'] )
Real_Literal.accept = lambda _self,visitor: visitor.visit_Real_Literal(_self)

Identifier = namedtuple( "Identifier", ['symbol'] )
Identifier.accept = lambda _self,visitor: visitor.visit_Identifier(_self)

# Simple arithmetic expression nodes
Binary_Operator_Node = namedtuple( "Binary_Operator_Node", ['op','lhs','rhs'] )
Binary_Operator_Node.accept = lambda _self,visitor: visitor.visit_Binary_Operator(_self)

Unary_Operator_Node = namedtuple( "Unary_Operator_Node", ['op', 'exp'] )
Unary_Operator_Node.accept = lambda _self,visitor: visitor.visit_Unary_Operator(_self)

# Tuple_Expression = namedtuple("Tuple_Expression", ['elements'])

Type_List = namedtuple("Type_List", ['types'] )
Type_List.append = lambda _self, value: _self.types.append(value)
Type_List.prepend = lambda _self, value: _self.types.insert(0, value)

Closure_Type = namedtuple("Closure_Type", ['in_types', 'out_type'])

Let_Declaration_Node = namedtuple( "Let_Declaration_Node", ['id', 'type', 'init'] )
Let_Declaration_Node.accept = lambda _self, visitor: visitor.Let_Declaration_Node(_self)

Closure_Node = namedtuple("Closure_Node", ['closure_type', 'body'] )

Return_Statement = namedtuple("Return_Statement", ['value'])
