from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, root_validator, validator

from .services.utils.waardelijsten import BestuursorgaanSoort, ProcedureStappenDefinitief, Provincie


class FRBR(BaseModel, metaclass=ABCMeta):
    Work_Province_ID: str
    Work_Date: str
    Work_Other: str
    Expression_Language: str
    Expression_Date: str
    Expression_Version: Optional[int]

    @abstractmethod
    def get_work(self) -> str:
        pass

    @abstractmethod
    def get_expression_part(self) -> str:
        pass

    def get_expression(self) -> str:
        result: str = self.get_work()
        expression_part: str = self.get_expression_part()
        if expression_part is not "":
            result = f"{result}/{expression_part}"

        return result


# <FRBRWork>/akn/nl/bill/pv28/2023/omgevingsvisie-1</FRBRWork>
# <FRBRExpression>/akn/nl/bill/pv28/2023/omgevingsvisie-1/nld@2024-09-29;2</FRBRExpression>
class BillFRBR(FRBR):
    Work_Country: str

    def get_work(self) -> str:
        work: str = f"/akn/{self.Work_Country}/bill/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
        return work

    def get_expression_part(self) -> str:
        expression_part: str = f"{self.Expression_Language}@{self.Expression_Date}"
        if self.Expression_Version is not None:
            expression_part = f"{expression_part};{self.Expression_Version}"
        return expression_part


# <FRBRWork>/akn/nl/act/pv28/2023/omgevingsvisie-1</FRBRWork>
# <FRBRExpression>/akn/nl/act/pv28/2023/omgevingsvisie-1/nld@2024-09-29;2</FRBRExpression>
class ActFRBR(FRBR):
    Work_Country: str

    def get_work(self) -> str:
        work: str = f"/akn/{self.Work_Country}/act/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
        return work

    def get_expression_part(self) -> str:
        expression_part: str = f"{self.Expression_Language}@{self.Expression_Date}"
        if self.Expression_Version is not None:
            expression_part = f"{expression_part};{self.Expression_Version}"
        return expression_part


# <FRBRWork>/join/id/regdata/pv28/2024/3</FRBRWork>
# <FRBRExpression>/join/id/regdata/pv28/2024/3/nld@2024-01-30;1855</FRBRExpression>
class GioFRBR(FRBR):
    def get_work(self) -> str:
        work: str = f"/join/id/regdata/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
        return work

    def get_expression_part(self) -> str:
        expression_part: str = f"{self.Expression_Language}@{self.Expression_Date}"
        if self.Expression_Version is not None:
            expression_part = f"{expression_part};{self.Expression_Version}"
        return expression_part


# /join/id/proces/pv28/2024/instelling-programma-1
class DoelFRBR(FRBR):
    # Removing these base fields by declaring a default value
    Expression_Language: str = Field("")
    Expression_Date: str = Field("")
    Expression_Version: Optional[int] = Field(1)

    def get_work(self) -> str:
        work: str = f"/join/id/proces/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
        return work

    def get_expression_part(self) -> str:
        return ""


class ProcedureStap(BaseModel):
    soort_stap: ProcedureStappenDefinitief
    voltooid_op: str

    @validator("soort_stap", pre=True)
    def map_enum_value(cls, v):
        try:
            return ProcedureStappenDefinitief[v].value
        except KeyError:
            raise ValueError(f"{v} is geen valide ProcedureStap uit de waardelijst")


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


class DocumentType(str, Enum):
    PROGRAMMA = "Programma"
    OMGEVINGSVISIE = "Omgevingsvisie"


class Doel(BaseModel):
    jaar: str
    naam: str


class PublicationSettings(BaseModel):
    document_type: DocumentType
    datum_bekendmaking: str
    datum_juridisch_werkend_vanaf: str
    provincie_id: str
    soort_bestuursorgaan: BestuursorgaanSoort
    regeling_componentnaam: str
    provincie_ref: str = Provincie.Zuid_Holland.value
    dso_versioning: DSOVersion = Field(default_factory=DSOVersion)
    besluit_frbr: BillFRBR
    regeling_frbr: ActFRBR
    opdracht: PublicatieOpdracht
    doel: DoelFRBR

    @validator("document_type", pre=True, always=True)
    def _format_document_type(cls, v):
        return DocumentType[v]

    @validator("soort_bestuursorgaan", pre=True)
    def _format_soort_bestuursorgaan(cls, v):
        if v in BestuursorgaanSoort.__members__.values():
            return v
        try:
            return BestuursorgaanSoort[v].value
        except KeyError:
            raise ValueError(f"{v} is geen valide Bestuursorgaan uit de waardelijst")

    @root_validator(pre=True)
    def _generate_opdracht(cls, v):
        opdracht = PublicatieOpdracht(**v["opdracht"])
        v["opdracht"] = opdracht
        return v

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)


class RegelingMutatie(BaseModel):
    was_regeling_frbr: ActFRBR

    # wId's used by indentifiers, for example beleidskeuze-4 by that object
    # Although it should be possible to add custom identifiers
    bekend_wid_map: Dict[str, str]

    # All previously used wIds. Which are allowed to be used again
    # The main reason here is that we can not generate new wIds for old versions
    bekend_wids: List[str]
