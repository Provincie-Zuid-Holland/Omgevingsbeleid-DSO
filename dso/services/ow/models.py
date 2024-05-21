from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from .enums import OwProcedureStatus, OwObjectStatus
from .ow_id import check_ow_id_imowtype, IMOWTYPES


class OWObject(BaseModel):
    OW_ID: str
    status: Optional[OwObjectStatus] = None
    procedure_status: Optional[OwProcedureStatus] = None


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str


class OWRegelingsgebied(OWObject):
    ambtsgebied: str


class OWLocatie(OWObject):
    mapped_uuid: Optional[UUID]
    noemer: Optional[str] = None


class OWAmbtsgebied(OWLocatie):
    bestuurlijke_genzenverwijzing: BestuurlijkeGrenzenVerwijzing


class OWGebied(OWLocatie):
    mapped_geo_code: Optional[str]


class OWGebiedenGroep(OWLocatie):
    mapped_geo_code: Optional[str]
    gebieden: List[OWGebied] = []


class OWDivisie(OWObject):
    wid: str


class OWDivisieTekst(OWObject):
    wid: str


class OWTekstDeel(OWObject):
    """
    note: divisietekstref is used as single item list
    for now but IMOW spec allows listing multiple.

    TODO:
    - Using str ow_id ref with "type" now, better to make full object,
    for consistency, but change to state map needed first.

    Not yet supported:
    - thema
    - kaartaanduiding
    - hoofdlijnaanduiding
    - gebiedsaanwijzing
    """

    divisie: str  # imow DivisieRef / DivisieTekstRef
    locaties: List[str]  # imow LocatieRef

    @property
    def divisie_type(self) -> str:
        return check_ow_id_imowtype(self.divisie).value
