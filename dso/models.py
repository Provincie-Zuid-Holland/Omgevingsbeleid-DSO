from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, root_validator, validator

from .services.utils.waardelijsten import BestuursorgaanSoort, ProcedureStappen, Provincie


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
        if expression_part != "":
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


# <FRBRWork>/join/id/pubdata/pv28/2024/3</FRBRWork>
# <FRBRExpression>/join/id/pubdata/pv28/2024/3/nld@2024-01-30;1855</FRBRExpression>
#
# @todo: This can be merged with GioFRBR, where should be set what the publication instruction is
#           which determines the `collection` (pubdata/regdata)
# @see: https://koop.gitlab.io/STOP/standaard/1.3.0/identificatie_niet-tekst.html
# @see: https://koop.gitlab.io/STOP/standaard/1.3.0/EA_EC4DE25BFB1341e6B632337DAF9C2791.html#Pkg__9058BA66AF9F44fbA43752F65A2654AF
class PubdataFRBR(FRBR):
    def get_work(self) -> str:
        work: str = f"/join/id/pubdata/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
        return work

    def get_expression_part(self) -> str:
        expression_part: str = f"{self.Expression_Language}@{self.Expression_Date}"
        if self.Expression_Version is not None:
            expression_part = f"{expression_part};{self.Expression_Version}"
        return expression_part


# <FRBRWork>/akn/nl/doc/pv28/2023/kennisgeving-omgevingsvisie-1</FRBRWork>
# <FRBRExpression>/akn/nl/doc/pv28/2023/kennisgeving-omgevingsvisie-1/nld@2024-09-29;2</FRBRExpression>
class DocFRBR(FRBR):
    Work_Country: str

    def get_work(self) -> str:
        work: str = f"/akn/{self.Work_Country}/doc/{self.Work_Province_ID}/{self.Work_Date}/{self.Work_Other}"
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
    soort_stap: ProcedureStappen
    voltooid_op: str

    @validator("soort_stap", pre=True)
    def map_enum_value(cls, v):
        if v in ProcedureStappen.__members__.values():
            return v
        try:
            return ProcedureStappen[v].value
        except KeyError:
            raise ValueError(f"{v} is geen valide ProcedureStap uit de waardelijst")


class ProcedureVerloop(BaseModel):
    bekend_op: str
    stappen: List[ProcedureStap] = Field([])


class ContentType(str, Enum):
    GML = "application/gml+xml"
    XML = "application/xml"
    PDF = "application/pdf"
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
        if v in OpdrachtType.__members__.values():
            return v
        return OpdrachtType[v]


class DocumentType(str, Enum):
    PROGRAMMA = "Programma"
    OMGEVINGSVISIE = "Omgevingsvisie"


class InstellingDoel(BaseModel):
    frbr: DoelFRBR
    datum_juridisch_werkend_vanaf: Optional[str]


class InstrekkingDoel(BaseModel):
    frbr: DoelFRBR
    datum_juridisch_tot: str


class Intrekking(BaseModel):
    doel: InstrekkingDoel


class PublicationSettings(BaseModel):
    document_type: DocumentType
    datum_bekendmaking: str
    provincie_id: str
    soort_bestuursorgaan: BestuursorgaanSoort
    regeling_componentnaam: str
    provincie_ref: str = Provincie.Zuid_Holland.value
    dso_versioning: DSOVersion = Field(default_factory=DSOVersion)
    besluit_frbr: BillFRBR
    regeling_frbr: ActFRBR
    opdracht: PublicatieOpdracht
    instelling_doel: InstellingDoel
    intrekking: Optional[Intrekking] = Field(None)

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
    was_regeling_vrijetekst: str

    # wId's used by indentifiers, for example beleidskeuze-4 by that object
    # Although it should be possible to add custom identifiers
    bekend_wid_map: Dict[str, str]

    # All previously used wIds. Which are allowed to be used again
    # The main reason here is that we can not generate new wIds for old versions
    bekend_wids: List[str]


class OwIdMapping(BaseModel):
    gebieden: Dict[str, str] = Field(default_factory=dict)
    gebiedengroep: Dict[str, str] = Field(default_factory=dict)
    ambtsgebied: Dict[str, str] = Field(default_factory=dict)
    wid: Dict[str, str] = Field(default_factory=dict)
    regelingsgebied: Dict[str, str] = Field(default_factory=dict)


class OwTekstdeelMap(BaseModel):
    divisie: str = Field(default="")
    location: str = Field(default="")


class OwObjectMap(BaseModel):
    id_mapping: OwIdMapping = Field(default_factory=OwIdMapping)
    tekstdeel_mapping: Dict[str, OwTekstdeelMap] = Field(default_factory=dict)


class OwData(BaseModel):
    object_ids: List[str] = Field(default_factory=list)
    object_map: OwObjectMap = Field(default_factory=OwObjectMap)
