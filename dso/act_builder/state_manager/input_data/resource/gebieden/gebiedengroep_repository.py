import json
import uuid
from typing import Dict, List, Optional

from .types import GebiedenGroep


class GebiedengroepRepository:
    def __init__(self):
        self._groepen: Dict[str, GebiedenGroep] = {}

    def add(self, groep: dict) -> None:
        groep_id = groep["UUID"]
        self._groepen[groep_id] = GebiedenGroep.model_validate(groep)

    def add_list(self, groepen: List[dict]) -> None:
        for groep in groepen:
            self.add(groep)

    def add_from_dict(self, groepen: Dict[str, dict]) -> None:
        for _, groep in groepen.items():
            self.add(groep)

    def get_optional(self, idx: uuid.UUID) -> Optional[GebiedenGroep]:
        groep: Optional[GebiedenGroep] = self._groepen.get(str(idx))
        return groep

    def get(self, idx: uuid.UUID) -> GebiedenGroep:
        groep: Optional[GebiedenGroep] = self.get_optional(idx)
        if groep is None:
            raise RuntimeError(f"Can not find groep {idx}")
        return groep

    def get_by_code_optional(self, code: str) -> Optional[GebiedenGroep]:
        for g in self._groepen.values():
            if g.code == code:
                return g
        return None

    def get_by_code(self, code: str) -> GebiedenGroep:
        groep: Optional[GebiedenGroep] = self.get_by_code_optional(code)
        if groep is None:
            raise RuntimeError(f"Can not find groep {code}")
        return groep

    def get_new(self) -> List[GebiedenGroep]:
        return [g for g in self._groepen.values() if g.new]

    def all(self) -> List[GebiedenGroep]:
        return list(self._groepen.values())

    def is_empty(self) -> bool:
        return not self._groepen

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._groepen.items()}
