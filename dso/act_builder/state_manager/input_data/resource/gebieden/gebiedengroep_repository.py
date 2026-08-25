import json
import uuid

from .types import GebiedenGroep


class GebiedengroepRepository:
    def __init__(self):
        self._groepen: dict[str, GebiedenGroep] = {}

    def add(self, groep: GebiedenGroep) -> None:
        self._groepen[groep.uuid] = groep

    def get_optional(self, idx: uuid.UUID) -> GebiedenGroep | None:
        groep: GebiedenGroep | None = self._groepen.get(str(idx))
        return groep

    def get(self, idx: uuid.UUID) -> GebiedenGroep:
        groep: GebiedenGroep | None = self.get_optional(idx)
        if groep is None:
            raise RuntimeError(f"Can not find groep {idx}")
        return groep

    def get_by_code_optional(self, code: str) -> GebiedenGroep | None:
        for g in self._groepen.values():
            if g.code == code:
                return g
        return None

    def get_by_code(self, code: str) -> GebiedenGroep:
        groep: GebiedenGroep | None = self.get_by_code_optional(code)
        if groep is None:
            raise RuntimeError(f"Can not find groep {code}")
        return groep

    def all(self) -> list[GebiedenGroep]:
        return list(self._groepen.values())

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._groepen.items()}
