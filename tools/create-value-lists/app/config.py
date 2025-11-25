from typing import Set

# See: "Waardelijsten IMOW  [service als zip-bestand]" on this page: https://www.geonovum.nl/omgevingswet/STOPTPOD
DOWNLOAD_URL: str = "https://geonovum.github.io/TPOD/Waardelijsten/waardelijsten_IMOW_v4.3.0.zip"
SOURCE_FILE: str = "waardelijsten_IMOW_v4.3.0.json"

TARGET_FILE: str = "./dso/services/ow/area_designation/gen/__init__.py"

VAR_NAME_GA_OMGEVINGSVISIE_DATA = "GA_OMGEVINGSVISIE_DATA"
VAR_NAME_GA_PROGRAMMA_DATA = "GA_PROGRAMMA_DATA"

# Document type matrix from TPOD v3.0.0
# https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20231215/#6F231895
OMGEVINGSVISIE_GA_MATRIX: Set[str] = [
    "bodem",
    "defensie",
    "energievoorziening",
    "erfgoed",
    "externe veiligheid",
    "geluid",
    "geur",
    "landschap",
    "leiding",
    "lucht",
    "mijnbouw",
    "natuur",
    "recreatie",
    "ruimtelijk gebruik",
    "verkeer",
    "water en watersysteem",
]
PROGRAMMA_GA_MATRIX: Set[str] = [
    "bodem",
    "defensie",
    "energievoorziening",
    "erfgoed",
    "externe veiligheid",
    "geluid",
    "geur",
    "landschap",
    "leiding",
    "lucht",
    "mijnbouw",
    "natuur",
    "recreatie",
    "ruimtelijk gebruik",
    "verkeer",
    "water en watersysteem",
]
