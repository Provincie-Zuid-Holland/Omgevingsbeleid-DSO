from typing import List
from pydantic import BaseModel


# These models represent the source json and are for
# simplicity kept in their source language dutch


class Waarde(BaseModel):
    label: str
    term: str
    uri: str
    definitie: str
    toelichting: str
    bron: str
    domein: str
    deprecated: str

    def is_deprecated(self) -> bool:
        return self.deprecated != "false"


class Waarden(BaseModel):
    waarde: List[Waarde]


class Domein(BaseModel):
    label: str
    term: str
    uri: str
    omschrijving: str
    toelichting: str


class Domeinen(BaseModel):
    domein: Domein


class Waardelijst(BaseModel):
    label: str
    titel: str
    uri: str
    type: str
    omschrijving: str
    toelichting: str
    waarden: Waarden
    domeinen: Domeinen

    def get_key(self) -> str:
        return self.label.replace(" ", "_").lower()


class Waardelijsten(BaseModel):
    versie: str
    set: str
    waardelijst: List[Waardelijst]


class SourceResult(BaseModel):
    waardelijsten: Waardelijsten

    def get_by_label(self, label: str) -> Waardelijst:
        for w in self.waardelijsten.waardelijst:
            if w.label == label:
                return w

        raise RuntimeError(f"Entry '{label}' not found")

    def get_by_domain(self, domain: str) -> Waardelijst:
        for w in self.waardelijsten.waardelijst:
            if w.domeinen.domein.label == domain:
                return w

        raise RuntimeError(f"Entry with domain '{domain}' not found")
