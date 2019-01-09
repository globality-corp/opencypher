"""
Pattern building.

"""
from dataclasses import dataclass
from typing import Optional

from opencypher.ast import (
    MapLiteral,
    NodeLabel,
    NodePattern,
    NonEmptyList,
    PatternElement,
    PatternElementChain,
    RelationshipPattern,
    RelationshipPatternType,
    RelationshipDetail,
    RelTypeName,
    Variable,
)


def _node(variable: Optional[str] = None,
          *labels: str,
          properties: Optional[MapLiteral] = None) -> NodePattern:
    return NodePattern(
        variable=Variable(variable) if variable else None,
        labels=NonEmptyList(
            NodeLabel(labels[0]),
            *(
                NodeLabel(arg)
                for arg in labels[1:]
            ),
        ) if labels else None,
        properties=properties,
    )


@dataclass(frozen=True)
class RelationshipDetailBuilder:
    builder: "PatternElementBuilder"
    relationship_pattern: RelationshipPattern

    def node(self,
             variable: Optional[str] = None,
             *labels: str,
             properties: Optional[MapLiteral] = None) -> "PatternElementBuilder":

        self.builder.items.append(
            PatternElementChain(
                relationship_pattern=self.relationship_pattern,
                node_pattern=_node(variable, *labels, properties=properties)
            ),
        )
        return self.builder


class PatternElementBuilder(PatternElement):

    @classmethod
    def node(cls,
             variable: Optional[str] = None,
             *labels: str,
             properties: Optional[MapLiteral] = None) -> "PatternElementBuilder":

        return cls(
            node_pattern=_node(variable, *labels, properties=properties)
        )

    def rel(self,
            value: Optional[str] = None,
            *args: str,
            properties: Optional[MapLiteral] = None,
            pattern_type=RelationshipPatternType.NONE) -> RelationshipDetailBuilder:

        return RelationshipDetailBuilder(
            builder=self,
            relationship_pattern=RelationshipPattern(
                detail=RelationshipDetail(
                    variable=Variable(value) if value else None,
                    types=NonEmptyList(
                        RelTypeName(args[0]),
                        *(
                            RelTypeName(arg)
                            for arg in args[1:]
                        ),
                    ) if args else None,
                    properties=properties,
                ),
                pattern_type=pattern_type,
            ),
        )

    def rel_in(self,
               value: Optional[str] = None,
               *args: str,
               properties: Optional[MapLiteral] = None) -> RelationshipDetailBuilder:

        return self.rel(value, *args, properties=properties, pattern_type=RelationshipPatternType.IN)

    def rel_out(self,
                value: Optional[str] = None,
                *args: str,
                properties: Optional[MapLiteral] = None) -> RelationshipDetailBuilder:

        return self.rel(value, *args, properties=properties, pattern_type=RelationshipPatternType.OUT)


node = PatternElementBuilder.node
