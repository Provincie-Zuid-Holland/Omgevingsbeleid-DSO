import json
from pathlib import Path
from typing import List, Optional


class ThemaRegistry:
    _instance = None
    _data = None
    _imow_version = None
    _requested_version = None

    def __new__(cls, version: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        if version is not None:
            cls._instance._data = None  # force reload if version changes
            cls._instance._requested_version = version
        return cls._instance

    def __init__(self, version: Optional[str] = None):
        self._requested_version = version
        if self._data is None:
            self._load_data()

    def _get_latest_version(self) -> str:
        """Find the latest version from available files."""
        pattern = "waardelijsten_IMOW_v*.json"
        files = Path(__file__).parent.glob(pattern)
        versions = []
        for f in files:
            version = f.stem.split("v")[-1]  # select version number from filename
            versions.append(version)
        return max(versions, key=lambda v: [int(x) for x in v.split(".")])

    def _load_data(self):
        version = self._requested_version or self._get_latest_version()
        json_path = Path(__file__).parent / f"waardelijsten_IMOW_v{version}.json"

        if not json_path.exists():
            raise ValueError(f"Waardelijst version {version} not found")

        with open(json_path) as f:
            data = json.load(f)

        data = data["waardelijsten"]
        self._imow_version = data["versie"]

        self._data = next(section for section in data["waardelijst"] if section.get("label") == "thema")

        self._values = {
            item["uri"]: {
                "uri": item["uri"],
                "label": item["label"],
                "definitie": item.get("definitie"),
                "term": item.get("term"),
            }
            for item in self._data["waarden"]["waarde"]
        }

        self._label_to_uri = {item["label"]: item["uri"] for item in self._data["waarden"]["waarde"]}

    def get_version(self) -> str:
        return self._imow_version

    def get_all_themas(self) -> List[dict]:
        return list(self._values.values())

    def get_thema(self, uri: str) -> Optional[dict]:
        return self._values.get(uri)

    def validate_thema(self, uri: str) -> bool:
        return uri in self._values

    def get_uri_by_label(self, label: str) -> Optional[str]:
        return self._label_to_uri.get(label)

    def get_thema_by_label(self, label: str) -> Optional[dict]:
        uri = self.get_uri_by_label(label)
        return self.get_thema(uri) if uri else None

    def get_all_labels(self) -> List[str]:
        return list(self._label_to_uri.keys())
