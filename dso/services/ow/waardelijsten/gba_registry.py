from pathlib import Path
import json
from typing import List, Optional


class GebiedsaanwijzingRegistry:
    _instance = None
    _data = None
    _imow_version = None
    _requested_version = None
    _groepen_data = {}
    _groepen_label_to_uri = {}
    _type_to_groep_mapping = {}  

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

        # Load all groep sections
        groep_sections = [
            section for section in data["waardelijst"] 
            if section["label"].endswith("groep")
        ]
        
        for groep_section in groep_sections:
            groep_type = groep_section["label"]
            # Store groep data
            self._groepen_data[groep_type] = {
                item["uri"]: {
                    "uri": item["uri"],
                    "label": item["label"],
                    "definitie": item.get("definitie"),
                    "term": item.get("term"),
                    "symboolcode": item.get("symboolcode")
                }
                for item in groep_section["waarden"]["waarde"]
            }
            
            # Store label to URI mapping for this groep
            self._groepen_label_to_uri[groep_type] = {
                item["label"]: item["uri"]
                for item in groep_section["waarden"]["waarde"]
            }
            
            # Map type to groep based on naming convention
            # e.g., "recreatiegroep" maps to type with label "recreatie"
            type_label = groep_type.replace("groep", "").lower()
            matching_type_uri = next(
                (uri for uri, type_data in self._data.items() 
                 if type_data["label"].lower() == type_label),
                None
            )
            if matching_type_uri:
                self._type_to_groep_mapping[matching_type_uri] = groep_type

    def get_version(self) -> str:
        return self._imow_version

    def get_all_type_gebiedsaanwijzingen(self) -> List[dict]:
        return list(self._data.values())

    def get_type_gebiedsaanwijzing(self, uri: str) -> Optional[dict]:
        return self._data.get(uri)

    def validate_type_gebiedsaanwijzing(self, uri: str) -> bool:
        return uri in self._data

    def get_type_gebiedsaanwijzing_by_label(self, label: str) -> Optional[dict]:
        uri = self._label_to_uri.get(label)
        return self.get_type_gebiedsaanwijzing(uri) if uri else None

    def get_all_labels(self) -> List[str]:
        return list(self._label_to_uri.keys())

    # methods for groepen functionality
    def get_groepen_for_type(self, type_uri: str) -> List[dict]:
        groep_type = self._type_to_groep_mapping.get(type_uri)
        if not groep_type or groep_type not in self._groepen_data:
            return []
        return list(self._groepen_data[groep_type].values())

    def get_groep_labels_for_type(self, type_uri: str) -> List[str]:
        groep_type = self._type_to_groep_mapping.get(type_uri)
        if not groep_type or groep_type not in self._groepen_label_to_uri:
            return []
        return list(self._groepen_label_to_uri[groep_type].keys())

    def validate_groep_for_type(self, type_uri: str, groep_uri: str) -> bool:
        groep_type = self._type_to_groep_mapping.get(type_uri)
        if not groep_type or groep_type not in self._groepen_data:
            return False
        return groep_uri in self._groepen_data[groep_type]

    def get_groep_by_label(self, type_uri: str, groep_label: str) -> Optional[dict]:
        groep_type = self._type_to_groep_mapping.get(type_uri)
        if not groep_type or groep_type not in self._groepen_label_to_uri:
            return None
        groep_uri = self._groepen_label_to_uri[groep_type].get(groep_label)
        if not groep_uri:
            return None
        return self._groepen_data[groep_type].get(groep_uri)

    def get_all_groep_types(self) -> List[str]:
        return list(self._groepen_data.keys())
