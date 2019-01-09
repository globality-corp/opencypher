from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Iterable, Optional

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.properties import Properties
from opencypher.ast.values import RelTypeName, Variable


@dataclass(frozen=True)
class RelationshipDetail(Parameterized):
    variable: Optional[Variable] = None
    types: Optional[NonEmptyList[RelTypeName]] = None
    # omitted: range_literal
    properties: Optional[Properties] = None

    def __str__(self) -> str:
        if self.variable is not None:
            if self.types is not None:
                if self.properties is not None:
                    return f"[ {str(self.variable)} {stringify(self.types, '|')} {str(self.properties)} ]"
                else:
                    return f"[ {str(self.variable)} {stringify(self.types, '|')} ]"
            else:
                if self.properties is not None:
                    return f"[ {str(self.variable)} {str(self.properties)} ]"
                else:
                    return f"[ {str(self.variable)} ]"
        else:
            if self.types is not None:
                if self.properties is not None:
                    return f"[ {stringify(self.types, '|')} {str(self.properties)} ]"
                else:
                    return f"[ {stringify(self.types, '|')} ]"
            else:
                if self.properties is not None:
                    return f"[ {str(self.properties)} ]"
                else:
                    return f"[ ]"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.properties is not None:
            yield from self.properties.iter_parameters()


@dataclass(frozen=True)
class Arrow:
    left: str
    right: str


@unique
class RelationshipPatternType(Enum):
    BOTH = Arrow("<-", "->")
    IN = Arrow("-", "->")
    NONE = Arrow("-", "-")
    OUT = Arrow("<-", "-")

    @property
    def left(self):
        return self.value.left

    @property
    def right(self):
        return self.value.right


@dataclass(frozen=True)
class RelationshipPattern(Parameterized):
    pattern_type: RelationshipPatternType = RelationshipPatternType.NONE
    detail: RelationshipDetail = field(default_factory=RelationshipDetail)

    def __str__(self) -> str:
        return f"{self.pattern_type.left} {str(self.detail)} {self.pattern_type.right}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.detail.iter_parameters()
