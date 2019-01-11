"""
Pattern building.

"""
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence, Tuple, Union

from opencypher.ast import (
    MapLiteral,
    NodeLabel,
    NodePattern,
    NonEmptySequence,
    PatternElement,
    PatternElementChain,
    RangeLiteral,
    RelationshipPattern,
    RelationshipPatternType,
    RelationshipDetail,
    RelTypeName,
    Variable,
)
from opencypher.builder.expression import (
    parameters as build_parameters,
    properties as build_properties,
)


def _node(variable: Optional[str] = None,
          labels: Optional[Union[str, Sequence[str]]] = None,
          properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None) -> NodePattern:

    if isinstance(labels, str):
        labels = (labels, )

    if isinstance(properties, Mapping):
        properties = build_properties(
            build_parameters(
                name_prefix=variable,
                **properties,
            ),
        )

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
             labels: Optional[Union[str, Sequence[str]]] = None,
             properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None) -> "PatternElementBuilder":

        chain = PatternElementChain(
            relationship_pattern=self.relationship_pattern,
            node_pattern=_node(variable, labels=labels, properties=properties)
        )
        return PatternElementBuilder(
            node_pattern=self.builder.node_pattern,
            items=(*self.builder.items, chain) if self.builder.items else (chain, ),
        )


class PatternElementBuilder(PatternElement):

    @classmethod
    def node(cls,
             variable: Optional[str] = None,
             labels: Optional[Union[str, Sequence[str]]] = None,
             properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None) -> "PatternElementBuilder":

        return cls(
            node_pattern=_node(variable, labels=labels, properties=properties)
        )

    def rel(self,
            variable: Optional[str] = None,
            types: Optional[Union[str, Sequence[str]]] = None,
            properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None,
            length: Optional[Union[Tuple, Tuple[int], Tuple[int, int]]] = None,
            pattern_type=RelationshipPatternType.NONE) -> RelationshipDetailBuilder:

        if isinstance(types, str):
            types = (types, )

        if isinstance(properties, Mapping):
            properties = build_properties(
                build_parameters(
                    name_prefix=variable,
                    **properties,
                ),
            )

        return RelationshipDetailBuilder(
            builder=self,
            relationship_pattern=RelationshipPattern(
                detail=RelationshipDetail(
                    variable=Variable(variable) if variable else None,
                    types=NonEmptySequence(
                        RelTypeName(types[0]),
                        *(
                            RelTypeName(type_)
                            for type_ in types[1:]
                        ),
                    ) if types else None,
                    length=RangeLiteral(
                        start=length[0] if len(length) > 0 else None,
                        end=length[1] if len(length) > 1 else None,
                    ) if length is not None else None,
                    properties=properties,
                ),
                pattern_type=pattern_type,
            ),
        )

    def rel_in(self,
               variable: Optional[str] = None,
               types: Optional[Union[str, Sequence[str]]] = None,
               properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None,
               length: Optional[Union[Tuple, Tuple[int], Tuple[int, int]]] = None) -> RelationshipDetailBuilder:

        return self.rel(
            variable=variable,
            types=types,
            length=length,
            properties=properties,
            pattern_type=RelationshipPatternType.IN,
        )

    def rel_out(self,
                variable: Optional[str] = None,
                types: Optional[Union[str, Sequence[str]]] = None,
                properties: Optional[Union[MapLiteral, Mapping[str, str]]] = None,
                length: Optional[Union[Tuple[int], Tuple[int, int]]] = None) -> RelationshipDetailBuilder:

        return self.rel(
            variable=variable,
            types=types,
            length=length,
            properties=properties,
            pattern_type=RelationshipPatternType.OUT,
        )


node = PatternElementBuilder.node
