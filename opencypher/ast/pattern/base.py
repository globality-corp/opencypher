from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.pattern.node import NodePattern
from opencypher.ast.pattern.relationship import RelationshipPattern
from opencypher.ast.values import Variable


@dataclass(frozen=True)
class PatternElementChain(Parameterized):
    relationship_pattern: RelationshipPattern = field(default_factory=RelationshipPattern)
    node_pattern: NodePattern = field(default_factory=NodePattern)

    def __str__(self) -> str:
        return f"{str(self.relationship_pattern)} {str(self.node_pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.relationship_pattern.iter_parameters()
        yield from self.node_pattern.iter_parameters()


@dataclass(frozen=True)
class PatternElement(Parameterized):
    node_pattern: NodePattern = field(default_factory=NodePattern)
    items: List[PatternElementChain] = field(default_factory=list)

    def __str__(self) -> str:
        if self.items:
            return f"{str(self.node_pattern)} {stringify(self.items)}"
        else:
            return f"{str(self.node_pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.node_pattern.iter_parameters()
        for item in self.items:
            yield from item.iter_parameters()


AnonymousPatternPart = PatternElement


@dataclass(frozen=True)
class PatternPart(Parameterized):
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
    items: NonEmptyList[PatternPart]

    def __str__(self) -> str:
        return stringify(self.items, ", ")

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
