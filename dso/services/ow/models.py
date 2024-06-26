from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .enums import OwProcedureStatus


class OWObject(BaseModel):
    OW_ID: str
    procedure_status: Optional[OwProcedureStatus] = None


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str


class OWAmbtsgebied(OWObject):
    bestuurlijke_genzenverwijzing: BestuurlijkeGrenzenVerwijzing
    mapped_uuid: Optional[UUID]


class OWRegelingsgebied(OWObject):
    # locatieaanduiding ambtsgebied
    ambtsgebied: str


class OWLocation(OWObject):
    geo_uuid: UUID
    noemer: Optional[str] = None
    mapped_geo_code: Optional[str]


class OWGebied(OWLocation):
    OW_ID: str


class OWGebiedenGroep(OWLocation):
    OW_ID: str
    locations: List[OWGebied] = []


class OWDivisie(OWObject):
    OW_ID: str
    wid: str


class OWDivisieTekst(OWObject):
    OW_ID: str
    wid: str


class OWTekstDeel(OWObject):
    OW_ID: str
    divisie: Optional[str]  # is divisie(tekst) OW_ID
    locations: List[str]  # OWlocation OW_ID list


class Annotation(BaseModel):
    """
    XML data wrapper for OWDivisie and OWTekstDeel objects as annotation in OwDivisie.
    """

    divisie_aanduiding: Optional[OWDivisie] = None
    divisietekst_aanduiding: Optional[OWDivisieTekst] = None
    tekstdeel: OWTekstDeel
