from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Iterable, Optional, Union

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import RelationshipTypes, Variable
from opencypher.ast.properties import Properties


@dataclass(frozen=True)
class RelationshipDetail(Parameterized):
    """
    RelationshipDetail = '[', [SP], [Variable, [SP]], [RelationshipTypes, [SP]], [RangeLiteral], [Properties, [SP]], ']' ;  # noqa: E501

    """
    variable: Optional[Variable] = None
    types: Optional[RelationshipTypes] = None
    # omitted: range_literal
    properties: Optional[Properties] = None

    def __str__(self) -> str:
        if self.variable is not None:
            if self.types is not None:
                if self.properties is not None:
                    return f"[ {str(self.variable)} {str_join(self.types, '|')} {str(self.properties)} ]"
                else:
                    return f"[ {str(self.variable)} {str_join(self.types, '|')} ]"
            else:
                if self.properties is not None:
                    return f"[ {str(self.variable)} {str(self.properties)} ]"
                else:
                    return f"[ {str(self.variable)} ]"
        else:
            if self.types is not None:
                if self.properties is not None:
                    return f"[ {str_join(self.types, '|')} {str(self.properties)} ]"
                else:
                    return f"[ {str_join(self.types, '|')} ]"
            else:
                if self.properties is not None:
                    return f"[ {str(self.properties)} ]"
                else:
                    return f"[ ]"

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
