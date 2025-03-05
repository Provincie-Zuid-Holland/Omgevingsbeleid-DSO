from typing import List

from pydantic import BaseModel, field_validator

from ....services.utils.waardelijsten import OnderwerpType, RechtsgebiedType


class Regeling(BaseModel):
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: str
    rechtsgebieden: List[RechtsgebiedType]
    onderwerpen: List[OnderwerpType]

    @field_validator("rechtsgebieden", mode="before")
    def _format_rechtsgebieden(cls, v):
        result = []
        for entry in v:
            if entry in RechtsgebiedType.__members__.values():
                result.append(entry)
            else:
                result.append(RechtsgebiedType[entry])
        return result

    @field_validator("onderwerpen", mode="before")
    def _format_onderwerpen(cls, v):
        result = []
        for entry in v:
            if entry in OnderwerpType.__members__.values():
                result.append(entry)
            else:
                result.append(OnderwerpType[entry])
        return result

    @field_validator("is_officieel", mode="before")
    def _format_is_officieel(cls, v):
        return str(v).lower()
