from dataclasses import dataclass
from enum import Enum


class ArtikelEidType(str, Enum):
    WIJZIG = "WIJZIG"
    TEKST = "TEKST"
    BESLUIT_INWERKINGSTIJD = "BESLUIT_INWERKINGSTIJD"
    REGELING_UITWERKINGSTIJD = "REGELING_UITWERKINGSTIJD"


@dataclass
class ArtikelEidData:
    eid: str
    artikel_type: ArtikelEidType

    def to_dict(self):
        return {
            "eid": self.eid,
            "artikel_type": self.artikel_type,
        }


class ArtikelEidRepository:
    def __init__(self):
        self._data: list[ArtikelEidData] = []

    def add(self, eid: str, artikel_type: ArtikelEidType):
        self._data.append(
            ArtikelEidData(
                eid=eid,
                artikel_type=artikel_type,
            )
        )

    def find_by_type(self, artikel_type: ArtikelEidType) -> list[ArtikelEidData]:
        results: list[ArtikelEidData] = [d for d in self._data if d.artikel_type == artikel_type]
        return results

    def find_one_by_type(self, artikel_type: ArtikelEidType) -> ArtikelEidData:
        results: list[ArtikelEidData] = self.find_by_type(artikel_type)
        match results:
            case [x]:
                return x
            case []:
                raise RuntimeError(f"No eid data found for artikel_type {artikel_type}")
            case _:
                raise RuntimeError(f"More then one eid data found for artikel_type {artikel_type}")

    def to_dict(self):
        return [d.to_dict() for d in self._data]
