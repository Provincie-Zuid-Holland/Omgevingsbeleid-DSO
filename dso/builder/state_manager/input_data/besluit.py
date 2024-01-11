from typing import List

from pydantic import BaseModel, validator

from ....services.utils.waardelijsten import OnderwerpType, ProcedureType, RechtsgebiedType


class Artikel(BaseModel):
    label: str
    inhoud: str


class Besluit(BaseModel):
    officiele_titel: str
    regeling_opschrift: str
    aanhef: str
    wijzig_artikel: Artikel
    tekst_artikelen: List[Artikel]
    tijd_artikel: Artikel
    sluiting: str
    ondertekening: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]
    soort_procedure: ProcedureType

    @validator("rechtsgebieden", pre=True, always=True)
    def _format_rechtsgebieden(cls, v):
        return [RechtsgebiedType[i] for i in v]

    @validator("onderwerpen", pre=True, always=True)
    def _format_onderwerpen(cls, v):
        return [OnderwerpType[i] for i in v]

    @validator("soort_procedure", pre=True, always=True)
    def _format_soort_procedure(cls, v):
        return ProcedureType[v]
