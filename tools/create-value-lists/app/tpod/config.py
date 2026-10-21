# See: "Waardelijsten IMOW [service als zip-bestand]" on this page: https://www.geonovum.nl/omgevingswet/STOPTPOD
DOWNLOAD_URL: str = "https://github.com/Geonovum/TPOD-waardelijsten/raw/bc085eaa2cd3c7f7120486b271609be415aa5e2a/2026-10-20/waardelijsten_IMOW_6.0.1.zip"
SOURCE_FILE: str = "waardelijsten IMOW 6.0.1.json"

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
