# See: Waardelijsten KOOP on this page view all versions https://koop.gitlab.io/stop/standaard/index.html
from typing import List, Dict

from pydantic import BaseModel

DOWNLOAD_URL: str = "https://gitlab.com/koop/STOP/standaard/-/archive/[version]/"
DOWNLOAD_FILE: str = "standaard-[version].zip"
VERSION = "1.3.0"
SOURCE_FOLDER: str = "waardelijsten"

TARGET_FILE: str = "./dso/services/koop/waardelijsten/gen/__init__.py"

XML_NAMESPACES: Dict[str, str] = {"rsc": "https://standaarden.overheid.nl/stop/imop/resources/"}

IGNORE_FILES: List[str] = [
    "bekendmakingsblad",
    "gemeente",
    "ministerie",
    "overheidsthema",
    "soortgepubliceerdwork",
    "waterschap",
]

NAME_MAPPING: Dict[str, str] = {
    "Besluitvormingsprocedures": "ProcedureType",
    "Bestuursorganen": "BestuursorgaanType",
    "BWB-rechtgebied": "RechtsgebiedType",
    "Provincies": "Provincie",
    "Stappen uit de besluitvormingsprocedure voor een definitief besluit": "ProcedureStappenDefinitief",
    "Stappen uit de besluitvormingsprocedure voor een ontwerpbesluit": "ProcedureStappenOntwerp",
    "TOP-lijst": "OnderwerpType",
    "Typering van informatieobjecten naar dataformaat": "InformatieObjectType",
    "Typering van publicaties": "PublicatieType",
    "Typering van regelingen": "RegelingType",
    "worktypes": "WorkType",
}


class MergeTypes(BaseModel):
    name: str
    koop_types: List[str]


MERGE_TYPES: List[MergeTypes] = [
    MergeTypes(
        name="ProcedureStappen",
        koop_types=[
            "ProcedureStappenDefinitief",
            "ProcedureStappenOntwerp",
        ],
    )
]
