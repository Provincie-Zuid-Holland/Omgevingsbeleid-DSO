import json

from .types import Gio


class GioRepository:
    def __init__(self):
        self._gios: list[Gio] = []

    def add(self, gio: Gio) -> None:
        self._gios.append(gio)

    def get_by_key_optional(self, key: str) -> Gio | None:
        for g in self._gios:
            if g.key == key:
                return g
        return None

    def get_by_key(self, key: str) -> Gio:
        gio: Gio | None = self.get_by_key_optional(key)
        if gio is None:
            raise RuntimeError(f"Can not find Gio {key}")
        return gio

    def get_new(self) -> list[Gio]:
        return [w for w in self._gios if w.new]

    def all(self) -> list[Gio]:
        return list(self._gios)

    def is_empty(self) -> bool:
        return not self._gios

    def to_dict(self):
        return [json.loads(g.model_dump_json()) for g in self._gios]

    def add_from_dict(self, gios: list[dict]) -> None:
        for gio_dict in gios:
            gio: Gio = Gio.model_validate(gio_dict)
            self.add(gio)
