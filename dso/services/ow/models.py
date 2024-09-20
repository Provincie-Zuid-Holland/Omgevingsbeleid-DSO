from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from .enums import OwObjectStatus, OwProcedureStatus
from .imow_waardelijsten import GEBIEDSAANWIJZING_TO_GROEP_MAPPING, TypeGebiedsaanwijzingEnum
from .ow_id import check_ow_id_imowtype


# Base OWObject class
class OWObject(BaseModel, ABC):
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
        # Add subclasses that allow reference to this obj


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str

    @validator("bestuurlijke_grenzen_id", pre=True, always=True)
    def convert_to_upper(cls, v):
        return v.upper() if isinstance(v, str) else v


class OWRegelingsgebied(OWObject):
    ambtsgebied: str  # OW id ref

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.ambtsgebied in used_ow_ids


class OWLocatie(OWObject, ABC):
    mapped_uuid: Optional[UUID] = None
    noemer: Optional[str] = None


class OWAmbtsgebied(OWLocatie):
    noemer: str
    bestuurlijke_grenzen_verwijzing: BestuurlijkeGrenzenVerwijzing

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWRegelingsgebied", set())


class OWGebied(OWLocatie):
    mapped_geo_code: Optional[str] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.OW_ID in reverse_ref_index.get("OWGebiedenGroep", set())


class OWGebiedenGroep(OWLocatie):
    mapped_geo_code: Optional[str] = None
    gebieden: List[str] = []

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        # tests us gebieden are used
        if not all(gebied_id in used_ow_ids for gebied_id in self.gebieden):
            return False
        # tests if tekstdeel parent exists
        textdeel_refs = reverse_ref_index.get("OWTekstdeel", set())
        if self.OW_ID not in textdeel_refs:
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

    @validator("type_", pre=True)
    def validate_type(cls, value):
        if isinstance(value, str):
            try:
                return TypeGebiedsaanwijzingEnum[value]
            except KeyError:
                for enum_member in TypeGebiedsaanwijzingEnum:
                    if enum_member.value == value:
                        return enum_member
        return value

    @validator("groep", pre=True)
    def validate_groep(cls, value, values):
        if "type_" in values:
            type_enum = values["type_"]
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
