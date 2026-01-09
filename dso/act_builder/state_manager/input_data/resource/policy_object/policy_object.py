import uuid
from datetime import datetime
from typing import Any, Optional


class PolicyObject:
    def __init__(self, data: dict):
        self.data: dict = data

    def get_data(self) -> dict:
        return self.data

    def get(self, key: str, default: Any = None):
        return self.data.get(key, default)

    def to_dict(self):
        serializable_dict = {}
        for key, value in self.data.items():
            if isinstance(value, uuid.UUID):
                serializable_dict[key] = str(value)
            elif isinstance(value, datetime):
                serializable_dict[key] = value.isoformat()
            else:
                serializable_dict[key] = value
        return serializable_dict

    def has_gebiedengroep(self) -> bool:
        """
        This case is a bit special.
        If "Gebiedengroep_Code" is not even defined as a property; then the object in not eligible for a Location
        If "Gebiedengroep_Code" is defined but None; then use ambtsgebied
        If "Gebiedengroep_Code" has content; Use that werkingsgebied

        This could be made clear with custom class hierarchy but seems overkill for now
        """
        return "Gebiedengroep_Code" in self.data

    def get_gebiedengroep_code(self) -> Optional[str]:
        return self.get("Gebiedengroep_Code")
