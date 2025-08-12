import json
import uuid
from typing import Dict, List, Optional

from .werkingsgebied import Werkingsgebied


class WerkingsgebiedRepository:
    def __init__(self):
        self._werkingsgebieden: Dict[str, Werkingsgebied] = {}

    def add(self, werkingsgebied: dict) -> None:
        werkingsgebied_id = werkingsgebied["UUID"]
        self._werkingsgebieden[werkingsgebied_id] = Werkingsgebied.model_validate(werkingsgebied)

    def add_list(self, werkingsgebieden: List[dict]) -> None:
        for werkingsgebied in werkingsgebieden:
            self.add(werkingsgebied)

    def add_from_dict(self, werkingsgebieden: Dict[str, dict]) -> None:
        for werkingsgebied_uuid, werkingsgebied in werkingsgebieden.items():
            self.add(werkingsgebied)

    def get_optional(self, idx: uuid.UUID) -> Optional[Werkingsgebied]:
        werkingsgebied: Optional[Werkingsgebied] = self._werkingsgebieden.get(str(idx))
        return werkingsgebied

    def get(self, idx: uuid.UUID) -> Werkingsgebied:
        werkingsgebied: Optional[Werkingsgebied] = self.get_optional(idx)
        if werkingsgebied is None:
            raise RuntimeError(f"Can not find werkingsgebied {idx}")
        return werkingsgebied

    def get_by_code_optional(self, code: str) -> Optional[Werkingsgebied]:
        for w in self._werkingsgebieden.values():
            if w.Code == code:
                return w
        return None

    def get_by_code(self, code: str) -> Werkingsgebied:
        werkingsgebied: Optional[Werkingsgebied] = self.get_by_code_optional(code)
        if werkingsgebied is None:
            raise RuntimeError(f"Can not find werkingsgebied {code}")
        return werkingsgebied

    def get_new(self) -> List[Werkingsgebied]:
        return [w for w in self._werkingsgebieden.values() if w.New]

    def all(self) -> List[Werkingsgebied]:
        return list(self._werkingsgebieden.values())

    def is_empty(self) -> bool:
        return not self._werkingsgebieden

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._werkingsgebieden.items()}
