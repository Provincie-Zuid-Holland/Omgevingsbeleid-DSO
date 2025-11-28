from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class OwInputAbstractLocatieRef(BaseModel):
    def get_code(self) -> Optional[str]:
        return None


class OwInputAmbtsgebiedLocatieRef(OwInputAbstractLocatieRef):
    pass


class OwInputGebiedengroepLocatieRef(OwInputAbstractLocatieRef):
    code: str

    def get_code(self) -> Optional[str]:
        return self.code


class OwInputGebied(BaseModel):
    source_uuid: str
    source_code: str
    title: str
    geometry_id: str


class OwInputAmbtsgebied(BaseModel):
    source_uuid: str
    administrative_borders_id: str
    domain: str
    valid_on: str
    title: str


class OwInputRegelingsgebied(BaseModel):
    source_uuid: str


class OwInputGebiedengroep(BaseModel):
    source_uuid: str
    source_code: str
    title: str
    gebieden: List[OwInputGebied]


class OwInputGebiedsaanwijzing(BaseModel):
    source_werkingsgebied_code: str
    title: str
    indication_type: str
    indication_group: str
    location_refs: List[OwInputAbstractLocatieRef]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_unique_key(self) -> str:
        return f"{self.source_werkingsgebied_code}-{self.indication_type}-{self.indication_group}"

    def __hash__(self):
        return hash((self.source_werkingsgebied_code, self.indication_type, self.indication_group))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.get_unique_key() == other.get_unique_key()


class OwInputPolicyObject(BaseModel):
    source_uuid: str
    source_code: str
    wid: str
    element: str
    location_refs: List[OwInputAbstractLocatieRef]

    model_config = ConfigDict(arbitrary_types_allowed=True)
