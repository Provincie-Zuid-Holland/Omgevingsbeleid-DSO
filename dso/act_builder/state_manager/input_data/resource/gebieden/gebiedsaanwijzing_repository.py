import json
from typing import Dict, List, Optional

from .types import Gebiedsaanwijzing


class GebiedsaanwijzingRepository:
    def __init__(self):
        self._data: Dict[str, Gebiedsaanwijzing] = {}

    def add(self, aanwijzing: Gebiedsaanwijzing) -> None:
        self._data[str(aanwijzing.uuid)] = aanwijzing

    def get_optional(self, uuid: str) -> Optional[Gebiedsaanwijzing]:
        aanwijzing: Optional[Gebiedsaanwijzing] = self._data.get(uuid)
        return aanwijzing

    def get(self, uuid: str) -> Gebiedsaanwijzing:
        aanwijzing: Optional[Gebiedsaanwijzing] = self.get_optional(uuid)
        if aanwijzing is None:
            raise RuntimeError(f"Can not find gebiedsaanwijzing {uuid}")
        return aanwijzing

    def all(self) -> List[Gebiedsaanwijzing]:
        return list(self._data.values())

    def is_empty(self) -> bool:
        return not self._data

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._data.items()}
