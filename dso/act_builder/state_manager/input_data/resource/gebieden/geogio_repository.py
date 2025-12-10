import json
from typing import List, Optional

from .types import GeoGio


class GeoGioRepository:
    def __init__(self):
        self._gios: List[GeoGio] = []

    def add(self, gio: dict) -> None:
        self._gios.append(GeoGio.model_validate(gio))

    def get_by_key_optional(self, key: str) -> Optional[GeoGio]:
        for g in self._gios:
            if g.key() == key:
                return g
        return None

    def get_by_key(self, key: str) -> GeoGio:
        gio: Optional[GeoGio] = self.get_by_key_optional(key)
        if gio is None:
            raise RuntimeError(f"Can not find GeoGio {key}")
        return gio

    def get_new(self) -> List[GeoGio]:
        return [w for w in self._gios if w.new]

    def all(self) -> List[GeoGio]:
        return list(self._gios)

    def is_empty(self) -> bool:
        return not self._gios

    def to_dict(self):
        return [json.loads(g.model_dump_json()) for g in self._gios]
