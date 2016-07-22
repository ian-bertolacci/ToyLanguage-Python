from __future__ import print_function
from collections import namedtuple

# Tokens / Leaf Nodes
Operator_Token = namedtuple( "Operator_Token", ['op'] )

Bool_Literal = namedtuple( "Bool_Literal", ['text','value'] )

Int_Literal = namedtuple( "Int_Literal", ['text','value'] )

Real_Literal = namedtuple( "Real_Literal", ['text','value'] )

Identifier = namedtuple( "Identifier", ['symbol'] )

# Simple arithmetic expression nodes
Binary_Operator_Node = namedtuple( "Binary_Operator_Node", ['op','lhs','rhs'] )

Unary_Operator_Node = namedtuple( "Unary_Operator_Node", ['op', 'exp'] )

# Type declarations
Typed_Id = namedtuple( "Typed_Id", ['id', 'id_type'] )

Type_List = namedtuple("Type_List", ['types'] )
Type_List.prepend = lambda self, value: self.types.insert(0, value)
Type_List.append = lambda self, value: self.types.append(value)

Typed_Id_List = namedtuple( "Typed_Id_List", ['typed_ids'] )
Typed_Id_List.prepend = lambda self, value: self.typed_ids.insert(0, value)
Typed_Id_List.append = lambda self, value: self.typed_ids.append(value)

Closure_Type = namedtuple("Closure_Type", ['in_types', 'out_type'] )

# Closures
Closure_Param_Decl = namedtuple( "Closure_Param_Decl", ['in_params', 'out_type'] )

Closure_Node = namedtuple("Closure_Node", ['closure_type', 'body'] )

Closure_Eval = namedtuple( "Closure_Eval", ['closure_exp', 'parameters'] )

Unnamed_Param = namedtuple( "Unnamed_Param", ['value'] )

Named_Param = namedtuple( "Named_Param", ['id', 'value'] )

# Statements
Let_Declaration_Node = namedtuple( "Let_Declaration_Node", ['typed_id', 'init'] )

Return_Statement = namedtuple("Return_Statement", ['value'])
