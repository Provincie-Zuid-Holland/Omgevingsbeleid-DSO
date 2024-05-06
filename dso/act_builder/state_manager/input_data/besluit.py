from typing import List, Optional

from pydantic import BaseModel, Field, validator

from ....services.utils.waardelijsten import OnderwerpType, ProcedureType, RechtsgebiedType


class Artikel(BaseModel):
    label: str = Field("Artikel")  # @deprecated
    nummer: str
    inhoud: str


class Bijlage(BaseModel):
    nummer: str
    opschrift: str
    content: str


class Motivering(BaseModel):
    opschrift: str
    content: str


class Besluit(BaseModel):
    officiele_titel: str
    citeertitel: Optional[str]
    aanhef: str
    wijzig_artikel: Artikel
    tekst_artikelen: List[Artikel]

    # tijd_artikel does not exist on drafts and should then be set to reserved
    tijd_artikel: Optional[Artikel]

    sluiting: str
    ondertekening: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]
    soort_procedure: ProcedureType
    bijlagen: List[Bijlage] = Field([])
    motivering: Optional[Motivering] = Field(None)

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
