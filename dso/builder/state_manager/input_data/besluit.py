from typing import List, Optional

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

    # tijd_artikel does not exist on drafts
    tijd_artikel: Optional[Artikel]

    sluiting: str
    ondertekening: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]
    soort_procedure: ProcedureType

    @validator("rechtsgebieden", pre=True, always=True)
    def _format_rechtsgebieden(cls, v):
        result = []
        for entry in v:
            if entry in RechtsgebiedType.__members__.values():
                result.append(entry)
            else:
                result.append(RechtsgebiedType[entry])
        return result

    @validator("onderwerpen", pre=True, always=True)
    def _format_onderwerpen(cls, v):
        result = []
        for entry in v:
            if entry in OnderwerpType.__members__.values():
                result.append(entry)
            else:
                result.append(OnderwerpType[entry])
        return result

    @validator("soort_procedure", pre=True, always=True)
    def _format_soort_procedure(cls, v):
        if v in ProcedureType.__members__.values():
            return v
        return ProcedureType[v]
