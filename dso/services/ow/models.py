from abc import abstractmethod
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from .enums import OwObjectStatus, OwProcedureStatus
from .waardelijsten.imow_waardelijsten import GEBIEDSAANWIJZING_TO_GROEP_MAPPING, TypeGebiedsaanwijzingEnum
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

    @validator("bestuurlijke_grenzen_id", pre=True, always=True)
    def convert_to_upper(cls, v):
        return v.upper() if isinstance(v, str) else v


class OWRegelingsgebied(OWObject):
    ambtsgebied: str  # OW id ref

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return self.ambtsgebied in used_ow_ids


class OWLocatie(OWObject):
    gio_ref: Optional[str] = None  # GeometrieRef -> GIO Identifier
    noemer: Optional[str] = None


class OWAmbtsgebied(OWObject):
    noemer: str
    bestuurlijke_grenzen_verwijzing: BestuurlijkeGrenzenVerwijzing
    mapped_uuid: Optional[UUID] = None

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
        return (
            all(gebied_id in used_ow_ids for gebied_id in self.gebieden) # no dead gebied refs
            and ( # has ref from tekstdeel or gebiedsaanwijzing
                self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())
                or self.OW_ID in reverse_ref_index.get("OWGebiedsaanwijzing", set())
            )
        )


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
    locaties: List[str] = Field(default_factory=list)
    gebiedsaanwijzingen: Optional[List[str]] = Field(default_factory=list)
    themas: List[str] = Field(default_factory=list)
    hoofdlijnen: List[str] = Field(default_factory=list)

    # idealisatie: Optional[str]
    # kaartaanduiding: Optional[str] = None

    @property
    def divisie_type(self) -> str:
        result = check_ow_id_imowtype(self.divisie).value
        return result

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return (
            self.divisie in used_ow_ids  # divisie exists
            and all(locatie_id in used_ow_ids for locatie_id in self.locaties)  # no dead location refs
            and all(gebiedsaanwijzing_id in used_ow_ids for gebiedsaanwijzing_id in (self.gebiedsaanwijzingen or [])) # no dead gebiedsaanwijzing refs
        )

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
        return (
            all(locatie_id in used_ow_ids for locatie_id in self.locaties) # no dead location refs
            and self.OW_ID in reverse_ref_index.get("OWTekstdeel", set()) # has ref from tekstdeel
        )


class OWHoofdlijn(OWObject):
    soort: str
    naam: str
    related_hoofdlijnen: Optional[List[str]] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        # TODO: check if related_hoofdlijnen are used in OWTekstdeel when supported
        return self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())
