from typing import Dict, List, Optional

from .hoofdlijn import Hoofdlijn


class HoofdlijnRepository:
    def __init__(self):
        self._hoofdlijnen: Dict[str, Hoofdlijn] = {}

    def add(self, hoofdlijn: dict):
        hoofdlijn: Hoofdlijn = Hoofdlijn.model_validate(hoofdlijn)
        self._hoofdlijnen[str(hoofdlijn.UUID)] = hoofdlijn

    def add_list(self, hoofdlijnen: List[dict]):
        for hoofdlijn in hoofdlijnen:
            self.add(hoofdlijn)

    def get_optional(self, uuidx: str) -> Optional[Hoofdlijn]:
        result: Optional[Hoofdlijn] = self._hoofdlijnen.get(uuidx)
        return result

    def get(self, uuidx: str) -> Hoofdlijn:
        result: Optional[Hoofdlijn] = self.get_optional(uuidx)
        if result is None:
            raise RuntimeError(f"Can not find hoofdlijn with uuid `{uuidx}`")
        return result

    def all(self) -> List[Hoofdlijn]:
        return list(self._hoofdlijnen.values())

    def is_empty(self) -> bool:
        return not self._hoofdlijnen

    def to_dict(self) -> Dict[str, str]:
        serializable_data = {str(k): v.get_title() for k, v in self._hoofdlijnen.items()}
        return serializable_data

    def get_by_codes(self, codes: List[str]) -> List[Hoofdlijn]:
        result: List[Hoofdlijn] = [d for _, d in self._hoofdlijnen.items() if d.Code in codes]
        return result

    def get_new(self) -> List[Hoofdlijn]:
        return [d for d in self._hoofdlijnen.values() if d.New]

    def add_from_dict(self, hoofdlijnen: List[dict]) -> None:
        for hoofdlijn_dict in hoofdlijnen:
            self.add(hoofdlijn_dict)
