from typing import List

from pydantic import BaseModel, validator

from ....services.utils.waardelijsten import OnderwerpType, RechtsgebiedType


class Regeling(BaseModel):
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]

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

    @validator("is_officieel", pre=True, always=True)
    def _format_is_officieel(cls, v):
        return str(v).lower()
