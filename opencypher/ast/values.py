from dataclasses import dataclass


SchemaName = str
SymbolicName = str


FunctionName = SymbolicName
LabelName = SchemaName
PropertyKeyName = SchemaName
Variable = SymbolicName


@dataclass(frozen=True)
class NodeLabel:
    value: LabelName

    def __str__(self) -> str:
        return f":{str(self.value)}"


@dataclass(frozen=True)
class RelTypeName:
    value: SchemaName

    def __str__(self) -> str:
        return f":{str(self.value)}"
