import json

from .types import Gebiedsaanwijzing


class GebiedsaanwijzingRepository:
    def __init__(self):
        self._data: dict[str, Gebiedsaanwijzing] = {}

    def add(self, aanwijzing: Gebiedsaanwijzing) -> None:
        self._data[str(aanwijzing.uuid)] = aanwijzing

    def get_optional(self, uuid: str) -> Gebiedsaanwijzing | None:
        aanwijzing: Gebiedsaanwijzing | None = self._data.get(uuid)
        return aanwijzing

    def get(self, uuid: str) -> Gebiedsaanwijzing:
        aanwijzing: Gebiedsaanwijzing | None = self.get_optional(uuid)
        if aanwijzing is None:
            raise RuntimeError(f"Can not find gebiedsaanwijzing {uuid}")
        return aanwijzing

    def get_by_code_optional(self, code: str) -> Gebiedsaanwijzing | None:
        for aanwijzing in self._data.values():
            if aanwijzing.code == code:
                return aanwijzing
        return None

    def get_by_code(self, code: str) -> Gebiedsaanwijzing:
        aanwijzing: Gebiedsaanwijzing | None = self.get_by_code_optional(code)
        if aanwijzing is None:
            raise RuntimeError(f"Can not find gebiedsaanwijzing {code}")
        return aanwijzing

    def all(self) -> list[Gebiedsaanwijzing]:
        return list(self._data.values())

    def is_empty(self) -> bool:
        return not self._data

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._data.items()}

    def add_from_dict(self, gebiedsaanwijzingen: list[dict]) -> None:
        for gebiedsaanwijzing_dict in gebiedsaanwijzingen:
            gebiedsaanwijzing: Gebiedsaanwijzing = Gebiedsaanwijzing.model_validate(gebiedsaanwijzing_dict)
            self.add(gebiedsaanwijzing)
