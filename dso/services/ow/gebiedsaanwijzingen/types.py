from typing import List
from pydantic import BaseModel, Field


class GebiedsaanwijzingWaarde(BaseModel):
    label: str
    term: str
    uri: str
    definitie: str
    toelichting: str
    bron: str
    domein: str
    deprecated: bool


class GebiedsaanwijzingType(BaseModel):
    label: str
    term: str
    uri: str
    definitie: str
    bron: str
    domein: str
    deprecated: bool


class GebiedsaanwijzingGroep(BaseModel):
    label: str
    titel: str
    uri: str
    omschrijving: str
    toelichting: str


class Gebiedsaanwijzing(BaseModel):
    aanwijzing_type: GebiedsaanwijzingType
    aanwijzing_groep: GebiedsaanwijzingGroep
    waardes: List[GebiedsaanwijzingWaarde] = Field(default_factory=list)

    def get_value_labels(self) -> List[str]:
        result: List[str] = [w.label for w in self.waardes]
        return result
