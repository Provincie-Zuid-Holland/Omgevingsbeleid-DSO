import json
import uuid
from typing import Dict, List, Optional

from .types import Gebiedsaanwijzing


class GebiedsaanwijzingRepository:
    def __init__(self):
        self._data: Dict[str, Gebiedsaanwijzing] = {}

    def add(self, aanwijzing: dict) -> None:
        aanwijzing_id = aanwijzing["uuid"]
        self._data[aanwijzing_id] = Gebiedsaanwijzing.model_validate(aanwijzing)

    def add_list(self, aanwijzingen: List[dict]) -> None:
        for aanwijzing in aanwijzingen:
            self.add(aanwijzing)

    def get_optional(self, idx: uuid.UUID) -> Optional[Gebiedsaanwijzing]:
        aanwijzing: Optional[Gebiedsaanwijzing] = self._data.get(str(idx))
        return aanwijzing

    def get(self, idx: uuid.UUID) -> Gebiedsaanwijzing:
        aanwijzing: Optional[Gebiedsaanwijzing] = self.get_optional(idx)
        if aanwijzing is None:
            raise RuntimeError(f"Can not find gebiedsaanwijzing {idx}")
        return aanwijzing

    def all(self) -> List[Gebiedsaanwijzing]:
        return list(self._data.values())

    def is_empty(self) -> bool:
        return not self._data

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._data.items()}
