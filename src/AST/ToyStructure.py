from __future__ import print_function
from collections import namedtuple

# Tokens / Leaf Nodes
Operator_Token = namedtuple( "Operator_Token", ['op'] )

Bool_Literal = namedtuple( "Bool_Literal", ['text','value'] )

Int_Literal = namedtuple( "Int_Literal", ['text','value'] )

Real_Literal = namedtuple( "Real_Literal", ['text','value'] )

Identifier = namedtuple( "Identifier", ['symbol'] )

# Simple operator expression nodes
Binary_Operator_Expression = namedtuple( "Binary_Operator_Expression", ['op','lhs','rhs'] )

Unary_Operator_Expression = namedtuple( "Unary_Operator_Expression", ['op', 'expression'] )

If_Expression = namedtuple( "If_Expression", ['condition', 'then_body', 'else_body'] )

# Type declarations
Typed_Id = namedtuple( "Typed_Id", ['id', 'id_type'] )

Type_List = namedtuple( "Type_List", ['types'] )
Type_List.prepend = lambda self, value: self.types.insert(0, value)
Type_List.append = lambda self, value: self.types.append(value)

Typed_Id_List = namedtuple( "Typed_Id_List", ['typed_ids'] )
Typed_Id_List.prepend = lambda self, value: self.typed_ids.insert(0, value)
Typed_Id_List.append = lambda self, value: self.typed_ids.append(value)

Closure_Type = namedtuple( "Closure_Type", ['in_types', 'out_type'] )

# Closures
Closure_Parameter_Declaration = namedtuple( "Closure_Parameter_Declaration", ['in_params', 'out_type'] )

Closure = namedtuple( "Closure", ['closure_type', 'body'] )

Closure_Evaluation = namedtuple( "Closure_Evaluation", ['closure_expression', 'parameters'] )

Unnamed_Parameter = namedtuple( "Unnamed_Parameter", ['value'] )

Named_Parameter = namedtuple( "Named_Parameter", ['id', 'value'] )

# Statements
Let_Declaration = namedtuple( "Let_Declaration", ['typed_id', 'init'] )

Return_Statement = namedtuple( "Return_Statement", ['value'] )

If_Statement = namedtuple( "If_Statement", ['condition', 'then_body', 'else_body'] )
