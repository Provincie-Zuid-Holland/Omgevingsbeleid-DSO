from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .enums import OwObjectStatus, OwProcedureStatus
from .ow_id import check_ow_id_imowtype


class OWObject(BaseModel):
    OW_ID: str
    status: Optional[OwObjectStatus] = None
    procedure_status: Optional[OwProcedureStatus] = None

    def dict(self, **kwargs):
        # Add ow_type to dict for template level checks
        base_dict = super().dict(**kwargs)
        base_dict["ow_type"] = self.__class__.__name__
        return base_dict

    def set_status_beeindig(self):
        self.status = OwObjectStatus.BEEINDIG


class BestuurlijkeGrenzenVerwijzing(BaseModel):
    bestuurlijke_grenzen_id: str
    domein: str
    geldig_op: str


class OWRegelingsgebied(OWObject):
    ambtsgebied: str  # OW id ref


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


class OWTekstdeel(OWObject):
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
