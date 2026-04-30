from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from ....services.koop.waardelijsten.gen import Besluitvormingsprocedures, BwbRechtgebied, TopLijst


class Artikel(BaseModel):
    label: str = Field("Artikel")  # @deprecated
    nummer: str
    inhoud: str


class Bijlage(BaseModel):
    nummer: str
    opschrift: str
    content: str


class WijzigBijlage(BaseModel):
    nummer: str
    opschrift: str


class Motivering(BaseModel):
    nummer: Optional[str] = Field(None)
    opschrift: str
    content: str
    bijlagen: List[Bijlage] = Field(default_factory=list)


class Besluit(BaseModel):
    officiele_titel: str
    citeertitel: Optional[str] = Field(None)
    aanhef: str
    wijzig_artikel: Artikel
    wijzig_bijlage: WijzigBijlage = Field(
        WijzigBijlage(
            nummer="A",
            opschrift="bij Artikel I",
        )
    )
    tekst_artikelen: List[Artikel]

    # tijd_artikel does not exist on drafts and should then be set to reserved
    tijd_artikel: Optional[Artikel] = Field(None)

    sluiting: str
    ondertekening: str
    rechtsgebieden: List[BwbRechtgebied]
    onderwerpen: List[TopLijst]
    soort_procedure: Besluitvormingsprocedures
    bijlagen: List[Bijlage] = Field(default_factory=list)
    motivering: Optional[Motivering] = Field(None)

    @field_validator("rechtsgebieden", mode="before")
    def _format_rechtsgebieden(cls, value):
        result = []
        for entry in value:
            if entry in BwbRechtgebied.__members__.values():
                result.append(entry)
            else:
                result.append(BwbRechtgebied[entry])
        return result

    @field_validator("onderwerpen", mode="before")
    def _format_onderwerpen(cls, value):
        result = []
        for entry in value:
            if entry in TopLijst.__members__.values():
                result.append(entry)
            else:
                result.append(TopLijst[entry])
        return result

    @field_validator("soort_procedure", mode="before")
    def _format_soort_procedure(cls, value):
        if value in Besluitvormingsprocedures.__members__.values():
            return value
        return Besluitvormingsprocedures[value]
