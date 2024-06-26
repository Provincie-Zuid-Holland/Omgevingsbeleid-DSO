import uuid
from typing import Dict, List, Optional

from .werkingsgebied import Werkingsgebied


class WerkingsgebiedRepository:
    def __init__(self):
        self._werkingsgebieden: Dict[str, Werkingsgebied] = {}

    def add(self, werkingsgebied: dict):
        werkingsgebied_id = werkingsgebied["UUID"]
        self._werkingsgebieden[werkingsgebied_id] = Werkingsgebied.parse_obj(werkingsgebied)

    def add_list(self, werkingsgebieden: List[dict]):
        for werkingsgebied in werkingsgebieden:
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

    def all(self) -> List[Werkingsgebied]:
        return list(self._werkingsgebieden.values())

    def is_empty(self) -> bool:
        return not self._werkingsgebieden

    def to_dict(self):
        serializable_data = {str(k): v.json() for k, v in self._werkingsgebieden.items()}
        return serializable_data
