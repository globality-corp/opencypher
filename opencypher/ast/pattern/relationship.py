from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Callable, Iterable, Optional, Union

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import RelationshipTypes, Variable
from opencypher.ast.properties import Properties


@dataclass(frozen=True)
class RangeLiteral:
    """
    RangeLiteral = '*', [SP], [IntegerLiteral, [SP]], ['..', [SP], [IntegerLiteral, [SP]]] ;

    """
    start: Optional[int] = None
    end: Optional[int] = None

    def __str__(self) -> str:
        if self.start is None:
            return "*"
        elif self.end is None:
            return f"* {self.start}"
        else:
            return f"* {self.start} .. {self.end}"


@dataclass(frozen=True)
class RelationshipDetail(Parameterized):
    """
    RelationshipDetail = '[', [SP], [Variable, [SP]], [RelationshipTypes, [SP]], [RangeLiteral], [Properties, [SP]], ']' ;  # noqa: E501

    """
    variable: Optional[Variable] = None
    types: Optional[RelationshipTypes] = None
    length: Optional[RangeLiteral] = None
    properties: Optional[Properties] = None

    def __str__(self) -> str:
        terms = [self.variable, self.types, self.length, self.properties]
        funcs: Iterable[Callable[[Any], str]] = [str, lambda items: str_join(items, "|"), str, str]

        values = [
            func(term)
            for term, func in zip(terms, funcs)
            if term is not None
        ]

        if values:
            return f"[ {' '.join(values)} ]"
        else:
            return "[ ]"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.properties is not None:
            yield from self.properties.iter_parameters()


@unique
class ArrowHead(Enum):
    """
    Dash = '-'
     | 'Â­'
     | 'â€'
     | 'â€‘'
     | 'â€’'
     | 'â€“'
     | 'â€”'
     | 'â€•'
     | 'âˆ’'
     | 'ï¹˜'
     | 'ï¹£'
     | 'ï¼'
     ;

    """
    Dash = "-"

    """
    RightArrowHead = '>'
               | 'âŸ©'
               | 'ã€‰'
               | 'ï¹¥'
               | 'ï¼ž'
               ;

    """
    RightArrowHead = ">"

    """
    LeftArrowHead = '<'
              | 'âŸ¨'
              | 'ã€ˆ'
              | 'ï¹¤'
              | 'ï¼œ'
              ;

    """
    LeftArrowHead = "<"

    def __add__(self, value: "ArrowHead") -> str:
        return str(self) + str(value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Arrow:
    left: Union[ArrowHead, str]
    right: Union[ArrowHead, str]


@unique
class RelationshipPatternType(Enum):
    BOTH = Arrow(ArrowHead.LeftArrowHead + ArrowHead.Dash, ArrowHead.Dash + ArrowHead.RightArrowHead)
    IN = Arrow(ArrowHead.Dash, ArrowHead.Dash + ArrowHead.RightArrowHead)
    NONE = Arrow(ArrowHead.Dash, ArrowHead.Dash)
    OUT = Arrow(ArrowHead.LeftArrowHead + ArrowHead.Dash, ArrowHead.Dash)

    @property
    def left(self) -> str:
        return self.value.left

    @property
    def right(self) -> str:
        return self.value.right


@dataclass(frozen=True)
class RelationshipPattern(Parameterized):
    """
    RelationshipPattern = (LeftArrowHead, [SP], Dash, [SP], [RelationshipDetail], [SP], Dash, [SP], RightArrowHead)
                        | (LeftArrowHead, [SP], Dash, [SP], [RelationshipDetail], [SP], Dash)
                        | (Dash, [SP], [RelationshipDetail], [SP], Dash, [SP], RightArrowHead)
                        | (Dash, [SP], [RelationshipDetail], [SP], Dash)
                        ;

    """
    pattern_type: RelationshipPatternType = RelationshipPatternType.NONE
    detail: RelationshipDetail = field(default_factory=RelationshipDetail)

    def __str__(self) -> str:
        return f"{self.pattern_type.left} {str(self.detail)} {self.pattern_type.right}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.detail.iter_parameters()
