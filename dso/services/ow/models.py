from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import IMOWTYPES
from .ow_id import generate_ow_id


class OWObject(BaseModel):
    OW_ID: str


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str


class OWAmbtsgebied(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.REGELINGSGEBIED))
    bestuurlijke_genzenverwijzing: BestuurlijkeGrenzenVerwijzing


class OWRegelingsgebied(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.REGELINGSGEBIED))
    ambtsgebied: str  # locatieaanduiding ambtsgebied


class OWLocation(OWObject):
    geo_uuid: UUID
    noemer: Optional[str] = None


class OWGebied(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIED))


class OWGebiedenGroep(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIEDENGROEP))
    locations: List[OWGebied] = []


class OWDivisie(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.DIVISIE))
    wid: str


class OWDivisieTekst(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.DIVISIETEKST))
    wid: str


class OWTekstDeel(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.TEKSTDEEL))
    divisie: Optional[str]  # is divisie(tekst) OW_ID
    locations: List[str]  # OWlocation OW_ID list


class Annotation(BaseModel):
    """
    XML data wrapper for OWDivisie and OWTekstDeel objects as annotation in OwDivisie.
    """

    divisie_aanduiding: Optional[OWDivisie] = None
    divisietekst_aanduiding: Optional[OWDivisieTekst] = None
    tekstdeel: OWTekstDeel
