from abc import abstractmethod
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator

from .enums import OwObjectStatus, OwProcedureStatus
from .ow_id import check_ow_id_imowtype
# from .waardelijsten.imow_waardelijsten import GEBIEDSAANWIJZING_TO_GROEP_MAPPING, TypeGebiedsaanwijzingEnum
from .waardelijsten import GEBIEDSAANWIJZING_TO_GROEP_MAPPING
from .waardelijsten.waardelijsten import TYPE_GEBIEDSAANWIJZING_VALUES


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
        return all(
            gebied_id in used_ow_ids for gebied_id in self.gebieden
        ) and (  # no dead gebied refs  # has ref from tekstdeel or gebiedsaanwijzing
            self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())
            or self.OW_ID in reverse_ref_index.get("OWGebiedsaanwijzing", set())
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
            and all(
                gebiedsaanwijzing_id in used_ow_ids for gebiedsaanwijzing_id in (self.gebiedsaanwijzingen or [])
            )  # no dead gebiedsaanwijzing refs
        )

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["divisie_type"] = self.divisie_type
        return base_dict


class OWGebiedsaanwijzing(OWObject):
    naam: str  # locatie/gio noemer
    type_: str 
    groep: str
    locaties: List[str]  # locatieaanduiding + LocatieRefs
    wid: str

    @validator("type_", pre=True)
    def validate_type(cls, value):
        for entry in TYPE_GEBIEDSAANWIJZING_VALUES.waarden.waarde:
            if value == entry.uri or value == entry.term or value == entry.label:
                return entry.uri
        raise ValueError(f"'{value}' is not a valid TypeGebiedsaanwijzing")

    @validator("groep", pre=True)
    def validate_groep(cls, value, values):
        if "type_" not in values:
            raise ValueError("type_ must be validated before groep")

        type_uri = values["type_"]
        groep_value_list = GEBIEDSAANWIJZING_TO_GROEP_MAPPING.get(type_uri)
        if not groep_value_list:
            raise ValueError(f"No groep mapping found for type '{type_uri}'")

        # search for a matching uri, term, or label in the groep_value_list
        for entry in groep_value_list.waarden.waarde:
            if value == entry.uri or value == entry.term or value == entry.label:
                return entry.uri

        raise ValueError(f"'{value}' is not a valid groep value for type '{type_uri}'")

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        return (
            all(locatie_id in used_ow_ids for locatie_id in self.locaties) and
            self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())
        )


class OWHoofdlijn(OWObject):
    soort: str
    naam: str
    related_hoofdlijnen: Optional[List[str]] = None

    def has_valid_refs(self, used_ow_ids: List[str], reverse_ref_index: Dict[str, Set[str]]) -> bool:
        # TODO: check if related_hoofdlijnen are used in OWTekstdeel when supported
        return self.OW_ID in reverse_ref_index.get("OWTekstdeel", set())
