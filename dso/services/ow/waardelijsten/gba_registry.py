from pathlib import Path
import json
from typing import List, Optional


class TypeGebiedsaanwijzingRegistry:
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
        """Get latest version from available files."""
        waardelijst_files = Path(__file__).parent.glob("waardelijsten_IMOW_v*.json")
        versions = [f.name.split("v")[1].replace(".json", "") for f in waardelijst_files]
        if not versions:
            raise ValueError("No waardelijst files found")
        return max(versions)

    def _load_data(self):
        version = self._requested_version or self._get_latest_version()
        json_path = Path(__file__).parent / f"waardelijsten_IMOW_v{version}.json"
        
        if not json_path.exists():
            raise ValueError(f"Waardelijst version {version} not found")

        with open(json_path) as f:
            data = json.load(f)
        
        data = data["waardelijsten"]
        self._imow_version = data["versie"]
        
        # Find the type gebiedsaanwijzing section
        type_gebiedsaanwijzing_section = next(
            (section for section in data["waardelijst"] if section["label"] == "type gebiedsaanwijzing"),
            None
        )
        
        if not type_gebiedsaanwijzing_section:
            raise ValueError("Type gebiedsaanwijzing section not found in waardelijst")

        # Create lookup dictionaries
        self._data = {
            item["uri"]: {
                "uri": item["uri"],
                "label": item["label"],
                "definitie": item.get("definitie"),
                "term": item.get("term")
            } 
            for item in type_gebiedsaanwijzing_section["waarden"]["waarde"]
        }

        self._label_to_uri = {
            item["label"]: item["uri"]
            for item in type_gebiedsaanwijzing_section["waarden"]["waarde"]
        }

    def get_version(self) -> str:
        """Get the version of the loaded IMOW waardelijst."""
        return self._imow_version

    def get_all_type_gebiedsaanwijzingen(self) -> List[dict]:
        """Get all type gebiedsaanwijzing values."""
        return list(self._data.values())

    def get_type_gebiedsaanwijzing(self, uri: str) -> Optional[dict]:
        """Get a specific type gebiedsaanwijzing by URI."""
        return self._data.get(uri)

    def validate_type_gebiedsaanwijzing(self, uri: str) -> bool:
        """Validate if a type gebiedsaanwijzing URI exists."""
        return uri in self._data

    def get_type_gebiedsaanwijzing_by_label(self, label: str) -> Optional[dict]:
        """Get a type gebiedsaanwijzing by its label."""
        uri = self._label_to_uri.get(label)
        return self.get_type_gebiedsaanwijzing(uri) if uri else None

    def get_all_labels(self) -> List[str]:
        """Get all available type gebiedsaanwijzing labels."""
        return list(self._label_to_uri.keys())
