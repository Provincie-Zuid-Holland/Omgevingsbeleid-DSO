from abc import ABC
from dataclasses import dataclass, field
from typing import List

from pydantic import BaseModel, field_validator

from ...models import BillFRBR, ContentType, DocFRBR, ProcedureVerloop, PublicatieOpdracht
from ...services.utils.waardelijsten import OnderwerpType


class ContentData(ABC):
    pass


class StrContentData(ContentData):
    def __init__(self, content: str):
        self.content: str = content


@dataclass
class OutputFile:
    filename: str
    content_type: ContentType
    content: ContentData
    options: dict = field(default_factory=dict)


class Kennisgeving(BaseModel):
    officiele_titel: str
    onderwerpen: List[OnderwerpType]
    mededeling_over_frbr: BillFRBR

    @field_validator("onderwerpen", mode="before")
    def _format_onderwerpen(cls, value):
        result = []
        for entry in value:
            if entry in OnderwerpType.__members__.values():
                result.append(entry)
            else:
                result.append(OnderwerpType[entry])
        return result


class InputData(BaseModel):
    provincie_id: str
    provincie_ref: str

    opdracht: PublicatieOpdracht

    bekendmaking_frbr: DocFRBR
    kennisgeving: Kennisgeving
    procedure_verloop: ProcedureVerloop

    kennisgeving_tekst: str
