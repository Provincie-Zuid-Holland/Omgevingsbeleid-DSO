# See: "Waardelijsten IMOW [service als zip-bestand]" on this page: https://www.geonovum.nl/omgevingswet/STOPTPOD
DOWNLOAD_URL: str = "https://github.com/Geonovum/TPOD-waardelijsten/raw/1e4c67c31e7b57c8334142386256ff665108c53f/2026-10-15/waardelijsten_IMOW_6.0.0.zip"
SOURCE_FILE: str = "waardelijsten IMOW 6.0.0.json"

TARGET_PATH: str = "./dso/services/ow/{name}/gen"
TARGET_FILE: str = "__init__.py"

VAR_NAME_GA_OMGEVINGSVISIE_DATA = "GA_OMGEVINGSVISIE_DATA"
VAR_NAME_GA_PROGRAMMA_DATA = "GA_PROGRAMMA_DATA"

# Document type matrix from TPOD v3.0.0
# https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20231215/#6F231895
OMGEVINGSVISIE_GA_MATRIX: list[str] = [
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
PROGRAMMA_GA_MATRIX: list[str] = [
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
