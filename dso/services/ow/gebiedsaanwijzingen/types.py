from pydantic import BaseModel


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
    waardes: list[GebiedsaanwijzingWaarde]

    def get_value_labels(self) -> list[str]:
        result: list[str] = [w.label for w in self.waardes]
        return result

    def get_value_by_label(self, label: str) -> GebiedsaanwijzingWaarde | None:
        for value in self.waardes:
            if value.label == label:
                return value
        return None
