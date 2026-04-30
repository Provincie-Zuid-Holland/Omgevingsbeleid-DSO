# See: Waardelijsten KOOP on this page view all versions https://koop.gitlab.io/stop/standaard/index.html
from typing import List, Dict

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
