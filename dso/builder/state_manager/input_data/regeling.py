from typing import List

from pydantic import BaseModel, validator

from dso.services.utils.waardelijsten import OnderwerpType, RechtsgebiedType


class Regeling(BaseModel):
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]

    @validator("rechtsgebieden", pre=True, always=True)
    def _format_rechtsgebieden(cls, v):
        return [RechtsgebiedType[i] for i in v]

    @validator("onderwerpen", pre=True, always=True)
    def _format_onderwerpen(cls, v):
        return [OnderwerpType[i] for i in v]

    @validator("is_officieel", pre=True, always=True)
    def _format_is_officieel(cls, v):
        return str(v).lower()
