from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import Variable
from opencypher.ast.pattern.node import NodePattern
from opencypher.ast.pattern.relationship import RelationshipPattern


@dataclass(frozen=True)
class PatternElementChain(Parameterized):
    """
    PatternElementChain = RelationshipPattern, [SP], NodePattern ;

    """
    relationship_pattern: RelationshipPattern = field(default_factory=RelationshipPattern)
    node_pattern: NodePattern = field(default_factory=NodePattern)

    def __str__(self) -> str:
        return f"{str(self.relationship_pattern)}{str(self.node_pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.relationship_pattern.iter_parameters()
        yield from self.node_pattern.iter_parameters()


@dataclass(frozen=True)
class PatternElement(Parameterized):
    """
    PatternElement = (NodePattern, { [SP], PatternElementChain })
                   | ('(', PatternElement, ')')
                   ;

    """
    node_pattern: NodePattern = field(default_factory=NodePattern)
    items: Optional[Sequence[PatternElementChain]] = None

    def __str__(self) -> str:
        if self.items:
            return f"{str(self.node_pattern)}{str_join(self.items, '')}"
        else:
            return f"{str(self.node_pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.node_pattern.iter_parameters()
        if self.items:
            for item in self.items:
                yield from item.iter_parameters()


"""
AnonymousPatternPart = PatternElement ;

"""
AnonymousPatternPart = PatternElement


@dataclass(frozen=True)
class PatternPart(Parameterized):
    """
    PatternPart = (Variable, [SP], '=', [SP], AnonymousPatternPart)
                | AnonymousPatternPart
                ;
    """
    pattern_element: AnonymousPatternPart = field(default_factory=AnonymousPatternPart)
    variable: Optional[Variable] = None

    def __str__(self) -> str:
        if self.variable:
            return f"{str(self.variable)} = {str(self.pattern_element)}"
        else:
            return f"{str(self.pattern_element)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern_element.iter_parameters()


@dataclass(frozen=True)
class Pattern(Parameterized):
    """
    Pattern = PatternPart, { [SP], ',', [SP], PatternPart } ;

    """
    items: NonEmptySequence[PatternPart]

    def __str__(self) -> str:
        return str_join(self.items, ", ")

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
