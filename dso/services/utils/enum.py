from enum import Enum
from typing import Type


def merge_enums(name: str, *enums: Type[Enum]) -> Type[Enum]:
    merged: dict[str, object] = {}

    for enum in enums:
        for member in enum:
            merged[member.name] = member.value

    return Enum(name, merged, type=str)
