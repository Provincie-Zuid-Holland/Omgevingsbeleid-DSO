import json
from typing import List, Optional

from .types import Gio


class GioRepository:
    def __init__(self):
        self._gios: List[Gio] = []

    def add(self, gio: dict) -> None:
        self._gios.append(Gio.model_validate(gio))

    def get_by_key_optional(self, key: str) -> Optional[Gio]:
        for g in self._gios:
            if g.key() == key:
                return g
        return None

    def get_by_key(self, key: str) -> Gio:
        gio: Optional[Gio] = self.get_by_key_optional(key)
        if gio is None:
            raise RuntimeError(f"Can not find Gio {key}")
        return gio

    def get_new(self) -> List[Gio]:
        return [w for w in self._gios if w.new]

    def all(self) -> List[Gio]:
        return list(self._gios)

    def is_empty(self) -> bool:
        return not self._gios

    def to_dict(self):
        return [json.loads(g.model_dump_json()) for g in self._gios]
