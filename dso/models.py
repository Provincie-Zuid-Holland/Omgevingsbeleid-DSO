from enum import Enum
from typing import List

from pydantic import BaseModel, Field, root_validator, validator

from dso.services.utils.waardelijsten import ProcedureStappenDefinitief, Provincie


# <FRBRWork>/akn/nl/bill/pv28/2023/2_2093</FRBRWork>
# <FRBRExpression>/akn/nl/bill/pv28/2023/2_2093/nld@2023-09-29;2093</FRBRExpression>
class FRBR(BaseModel):
    work: str
    expression: str

    @staticmethod
    def from_dict(document_type: str, overheid: str, data: dict):
        work = f"/akn/{data['work_land']}/{document_type}/{overheid}/{data['work_datum']}/{data['work_overig']}"
        expression = f"{work}/{data['expression_taal']}@{data['expression_datum']}"
        if "expression_versie" in data and data["expression_versie"]:
            expression = f"{expression};{data['expression_versie']}"
            if "expression_overig" in data and data["expression_overig"]:
                expression = f"{expression};{data['expression_overig']}"

        return FRBR(
            work=work,
            expression=expression,
        )


class ProcedureStap(BaseModel):
    soort_stap: ProcedureStappenDefinitief
    voltooid_op: str


class ProcedureVerloop(BaseModel):
    bekend_op: str
    stappen: List[ProcedureStap] = Field([])


class ContentType(str, Enum):
    GML = "application/gml+xml"
    XML = "application/xml"
    JPG = "image/jpeg"
    PNG = "image/png"


class Bestand(BaseModel):
    bestandsnaam: str
    content_type: str


class DSOVersion(BaseModel):
    STOP: str = "1.3.0"
    TPOD: str = "2.0.2"
    LVBB: str = "1.2.0"


class OpdrachtType(str, Enum):
    PUBLICATIE = "PUBLICATIE"
    VALIDATIE = "VALIDATIE"


class PublicatieOpdracht(BaseModel):
    opdracht_type: OpdrachtType
    id_levering: str = Field(..., max_length=80)

    """
    Het OIN van het Bevoegd Gezag waarvoor een gemandateerde/intermediair de afhandeling doet
    @link: https://koop.gitlab.io/lvbb/bronhouderkoppelvlak/1.2.0/lvbbt_xsd_Complex_Type_lvbbt_OpdrachtType.html#OpdrachtType_idBevoegdGezag
    """
    id_bevoegdgezag: str = Field(..., min_length=20, max_length=20)

    """
    OIN van BG zelf, indien geen intermediair van toepassing is.

    Als er wel een intermediair van toepassing is:

    OIN in het geval van samenwerkingsverband (overheidsorganisatie);
    HRN in het geval van softwareleverancier, die de berichten namens BG verstuurt

    @link: https://koop.gitlab.io/lvbb/bronhouderkoppelvlak/1.2.0/lvbbt_xsd_Complex_Type_lvbbt_OpdrachtType.html#OpdrachtType_idAanleveraar
    @link: https://www.logius.nl/diensten/oin
    """
    id_aanleveraar: str = "00000003011411800000"

    publicatie_bestand: str
    datum_bekendmaking: str

    @validator("opdracht_type", pre=True, always=True)
    def _format_opdracht_type(cls, v):
        return OpdrachtType[v]


class DocumentType(Enum):
    PROGRAMMA = "Omgevingsprogramma"
    VISIE = "Omgevingsvisie"


class Doel(BaseModel):
    jaar: str
    naam: str


class PublicationSettings(BaseModel):
    document_type: DocumentType
    datum_bekendmaking: str
    datum_juridisch_werkend_vanaf: str
    provincie_id: str
    wId_suffix: str
    soort_bestuursorgaan: str
    expression_taal: str
    regeling_componentnaam: str
    provincie_ref: str = Provincie.Zuid_Holland.value
    dso_versioning: DSOVersion = Field(default_factory=DSOVersion)
    besluit_frbr: FRBR
    regeling_frbr: FRBR
    opdracht: PublicatieOpdracht
    doel: Doel

    @validator("document_type", pre=True, always=True)
    def _format_document_type(cls, v):
        return DocumentType[v]

    @root_validator(pre=True)
    def _generate_besluit_frbr(cls, v):
        frbr = FRBR.from_dict(
            "bill",
            v["provincie_id"],
            v["besluit_frbr"],
        )
        v["besluit_frbr"] = frbr
        return v

    @root_validator(pre=True)
    def _generate_regeling_frbr(cls, v):
        frbr = FRBR.from_dict(
            "act",
            v["provincie_id"],
            v["regeling_frbr"],
        )
        v["regeling_frbr"] = frbr
        return v

    @root_validator(pre=True)
    def _generate_opdracht(cls, v):
        opdracht = PublicatieOpdracht(**v["opdracht"])
        v["opdracht"] = opdracht
        return v

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
