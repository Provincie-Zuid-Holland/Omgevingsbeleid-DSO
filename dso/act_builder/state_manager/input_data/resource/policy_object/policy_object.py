import uuid
from datetime import datetime
from typing import Any


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
        If "gebiedengroep_code" is not even defined as a property; then the object in not eligible for a Location
        If "gebiedengroep_code" is defined but None; then use ambtsgebied
        If "gebiedengroep_code" has content; Use that werkingsgebied

        This could be made clear with custom class hierarchy but seems overkill for now
        """
        return "gebiedengroep_code" in self.data

    def get_gebiedengroep_code(self) -> str | None:
        return self.get("gebiedengroep_code")

    def get_themas(self) -> list[str]:
        maybe_themas: list[str] | None = self.get("themas")
        if maybe_themas:
            return maybe_themas
        return []
