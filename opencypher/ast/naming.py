from dataclasses import dataclass

from opencypher.ast.collection import NonEmptySequence


"""
SchemaName = SymbolicName
           | ReservedWord
           ;

"""
# intentionally simplified
SchemaName = str

"""
SymbolicName = UnescapedSymbolicName
             | EscapedSymbolicName
             | HexLetter
             | (C,O,U,N,T)
             | (F,I,L,T,E,R)
             | (E,X,T,R,A,C,T)
             | (A,N,Y)
             | (N,O,N,E)
             | (S,I,N,G,L,E)
             ;

"""
# intentionally simplified
SymbolicName = str


"""
FunctionName = (Namespace, SymbolicName)
             | (E,X,I,S,T,S)
             ;

"""
# ommitted Namespace and EXISTS
FunctionName = SymbolicName


"""
LabelName = SchemaName ;

"""
LabelName = SchemaName


"""
PropertyKeyName = SchemaName ;

"""
PropertyKeyName = SchemaName


"""
Variable = SymbolicName ;

"""
Variable = SymbolicName


@dataclass(frozen=True)
class NodeLabel:
    """
    NodeLabel = ':', [SP], LabelName ;

    """
    value: LabelName

    def __str__(self) -> str:
        return f":{str(self.value)}"


"""
NodeLabels = NodeLabel, { [SP], NodeLabel } ;

"""
NodeLabels = NonEmptySequence[NodeLabel]


@dataclass(frozen=True)
class RelTypeName:
    """
    RelTypeName = SchemaName ;

    """
    value: SchemaName

    def __str__(self) -> str:
        """
        RelationshipTypes = ':', [SP], RelTypeName, { [SP], '|', [':'], [SP], RelTypeName } ;

        """
        # NB: we deviate slightly from the EBNF syntax and incorporating the colon prefix
        # from the `RelationshipTypes` grammar for simplicity: RelTypeName is *only* used in
        # this context and mergin these together simplifies string joining on '|'.
        return f":{str(self.value)}"


"""
RelationshipTypes = ':', [SP], RelTypeName, { [SP], '|', [':'], [SP], RelTypeName } ;

"""
# NB: the ':' is included in RelTypeName's __str__ function for simplicity
RelationshipTypes = NonEmptySequence[RelTypeName]
