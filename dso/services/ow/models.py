from abc import abstractmethod
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from .enums import OwObjectStatus, OwProcedureStatus
from .imow_waardelijsten import GEBIEDSAANWIJZING_TO_GROEP_MAPPING, TypeGebiedsaanwijzingEnum
from .ow_id import check_ow_id_imowtype


class OWObject(BaseModel):
    OW_ID: str
    status: Optional[OwObjectStatus] = None
    procedure_status: Optional[OwProcedureStatus] = None

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["ow_type"] = self.__class__.__name__
        return base_dict

    def set_status_beeindig(self):
        self.status = OwObjectStatus.BEEINDIG

    @abstractmethod
    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        """Check if current obj is actively referenced in the OW State"""


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str

    @field_validator("bestuurlijke_grenzen_id", mode="before")
    def convert_to_upper(cls, value):
        return value.upper() if isinstance(value, str) else value


class OWRegelingsgebied(OWObject):
    ambtsgebied: str  # OW id ref

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.ambtsgebied in used_ow_ids


class OWLocatie(OWObject):
    gio_ref: Optional[str] = None
    mapped_geo_code: Optional[str] = None
    noemer: str

    @model_validator(mode="before")
    def handle_legacy_gio_ref(cls, data):
        if "gio_ref" not in data and "mapped_uuid" in data:
            data["gio_ref"] = data.pop("mapped_uuid")
        return data


class OWAmbtsgebied(OWObject):
    noemer: str
    bestuurlijke_grenzen_verwijzing: BestuurlijkeGrenzenVerwijzing
    mapped_uuid: Optional[UUID] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWRegelingsgebied", set())


class OWGebied(OWLocatie):
    gio_ref: str
    noemer: str

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWGebiedenGroep", set())


class OWGebiedenGroep(OWLocatie):
    gebieden: List[str] = []

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        # tests if gebieden are used
        if not all(gebied_id in used_ow_ids for gebied_id in self.gebieden):
            return False
        # tests if referenced by tekstdeel or gebiedsaanwijzing
        tekstdeel_refs = reverse_ref_index.get("OWTekstdeel", set())
        gebiedsaanwijzing_refs = reverse_ref_index.get("OWGebiedsaanwijzing", set())
        if self.OW_ID not in tekstdeel_refs and self.OW_ID not in gebiedsaanwijzing_refs:
            return False
        return True


class OWDivisie(OWObject):
    wid: str
    mapped_policy_object_code: Optional[str] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())


class OWDivisieTekst(OWObject):
    wid: str
    mapped_policy_object_code: Optional[str] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())


class OWTekstdeel(OWObject):
    divisie: str  # imow DivisieRef / DivisieTekstRef
    locaties: List[str]  # imow LocatieRef
    gebiedsaanwijzingen: Optional[List[str]] = Field(default_factory=list)  # imow GebiedsaanwijzingRef

    # idealisatie: Optional[str]
    # thema: Optional[str] = None
    # kaartaanduiding: Optional[str] = None
    # hoofdlijnaanduiding: Optional[str] = None

    @property
    def divisie_type(self) -> str:
        result = check_ow_id_imowtype(self.divisie).value
        return result

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        if self.divisie not in used_ow_ids:
            return False
        if not all(locatie_id in used_ow_ids for locatie_id in self.locaties):
            return False
        if self.gebiedsaanwijzingen and not all(
            gebiedsaanwijzing_id in used_ow_ids for gebiedsaanwijzing_id in self.gebiedsaanwijzingen
        ):
            return False
        return True

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["divisie_type"] = self.divisie_type
        return base_dict


class OWGebiedsaanwijzing(OWObject):
    naam: str  # locatie/gio noemer
    type_: TypeGebiedsaanwijzingEnum  # TypeGebiedsaanwijzing waarde
    groep: str  # gebiedsaanwijzinggroep waarde
    locaties: List[str]  # locatieaanduiding + LocatieRefs
    wid: str

    @field_validator("type_", mode="before")
    def validate_type(cls, value):
        if isinstance(value, str):
            try:
                return TypeGebiedsaanwijzingEnum[value]
            except KeyError:
                for enum_member in TypeGebiedsaanwijzingEnum:
                    if enum_member.value == value:
                        return enum_member
        return value

    @field_validator("groep", mode="before")
    def validate_groep(cls, value, info: ValidationInfo):
        if "type_" in info.data:
            type_enum = info.data["type_"]
            groep_enum_class = GEBIEDSAANWIJZING_TO_GROEP_MAPPING[type_enum]
            if isinstance(value, str):
                try:
                    return groep_enum_class[value]
                except KeyError:
                    for enum_member in groep_enum_class:
                        if enum_member.value == value:
                            return enum_member
        raise ValueError(f"'{value}' is not a valid value for the groep field")

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        if not all(locatie_id in used_ow_ids for locatie_id in self.locaties):
            return False
        return True
