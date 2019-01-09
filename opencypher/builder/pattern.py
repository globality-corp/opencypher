"""
Pattern building.

"""
from dataclasses import dataclass
from typing import Optional

from opencypher.ast import (
    MapLiteral,
    NodeLabel,
    NodePattern,
    NonEmptySequence,
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
        labels=NonEmptySequence(
            NodeLabel(labels[0]),
            *(
                NodeLabel(label)
                for label in labels[1:]
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

        chain = PatternElementChain(
            relationship_pattern=self.relationship_pattern,
            node_pattern=_node(variable, *labels, properties=properties)
        )
        return PatternElementBuilder(
            node_pattern=self.builder.node_pattern,
            items=(*self.builder.items, chain) if self.builder.items else (chain, ),
        )


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
            *types: str,
            properties: Optional[MapLiteral] = None,
            pattern_type=RelationshipPatternType.NONE) -> RelationshipDetailBuilder:

        return RelationshipDetailBuilder(
            builder=self,
            relationship_pattern=RelationshipPattern(
                detail=RelationshipDetail(
                    variable=Variable(value) if value else None,
                    types=NonEmptySequence(
                        RelTypeName(types[0]),
                        *(
                            RelTypeName(type_)
                            for type_ in types[1:]
                        ),
                    ) if types else None,
                    properties=properties,
                ),
                pattern_type=pattern_type,
            ),
        )

    def rel_in(self,
               value: Optional[str] = None,
               *types: str,
               properties: Optional[MapLiteral] = None) -> RelationshipDetailBuilder:

        return self.rel(value, *types, properties=properties, pattern_type=RelationshipPatternType.IN)

    def rel_out(self,
                value: Optional[str] = None,
                *types: str,
                properties: Optional[MapLiteral] = None) -> RelationshipDetailBuilder:

        return self.rel(value, *types, properties=properties, pattern_type=RelationshipPatternType.OUT)


node = PatternElementBuilder.node
