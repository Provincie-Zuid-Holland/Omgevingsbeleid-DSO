from typing import Optional

from pydantic import BaseModel


class IMOWValue(BaseModel):
    label: str
    term: str
    uri: str
    definitie: Optional[str] = None

    def __str__(self) -> str:
        return self.uri


class ThemaValue(IMOWValue):
    pass


class TypeGebiedsaanwijzingValue(IMOWValue):
    @property
    def groep_label(self) -> str:
        """Returns the expected label for the corresponding group list"""
        return f"{self.term}groep"


class GebiedsaanwijzingGroepValue(IMOWValue):
    type_gebiedsaanwijzing: str  # URI of the related TypeGebiedsaanwijzing
