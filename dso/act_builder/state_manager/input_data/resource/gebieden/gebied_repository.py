import json
import uuid
from typing import Dict, List, Optional

from .types import Gebied, GebiedenGroep


class GebiedRepository:
    def __init__(self):
        self._gebieden: Dict[str, Gebied] = {}

    def add(self, gebied: dict) -> None:
        gebied_id = gebied["UUID"]
        self._gebieden[gebied_id] = Gebied.model_validate(gebied)

    def add_list(self, gebieden: List[dict]) -> None:
        for gebied in gebieden:
            self.add(gebied)

    def add_from_dict(self, gebieden: Dict[str, dict]) -> None:
        for gebied_uuid, gebied in gebieden.items():
            self.add(gebied)

    def get_optional(self, idx: uuid.UUID) -> Optional[Gebied]:
        gebied: Optional[Gebied] = self._gebieden.get(str(idx))
        return gebied

    def get(self, idx: uuid.UUID) -> Gebied:
        gebied: Optional[Gebied] = self.get_optional(idx)
        if gebied is None:
            raise RuntimeError(f"Can not find gebied {idx}")
        return gebied

    def get_by_code_optional(self, code: str) -> Optional[Gebied]:
        for g in self._gebieden.values():
            if g.code == code:
                return g
        return None

    def get_by_code(self, code: str) -> Gebied:
        gebied: Optional[Gebied] = self.get_by_code_optional(code)
        if gebied is None:
            raise RuntimeError(f"Can not find gebied {code}")
        return gebied

    def get_new(self) -> List[Gebied]:
        return [w for w in self._gebieden.values() if w.new]

    def all(self) -> List[Gebied]:
        return list(self._gebieden.values())

    def is_empty(self) -> bool:
        return not self._gebieden

    def get_for_group(self, group: GebiedenGroep) -> List[Gebied]:
        result: List[Gebied] = [gebied for gebied in self._gebieden.values() if gebied.code in group.area_codes]
        return result

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._gebieden.items()}
