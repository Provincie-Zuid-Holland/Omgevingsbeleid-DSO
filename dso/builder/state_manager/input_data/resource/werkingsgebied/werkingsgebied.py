import re
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, root_validator

from ......models import GioFRBR


class Locatie(BaseModel):
    UUID: uuid.UUID
    Title: str
    Symbol: str

    Gml: Optional[str] = Field(None)
    Geometry: Optional[str] = Field(None)

    @root_validator
    def _must_have_a_source(cls, v):
        if v["Gml"] is None and v["Geometry"] is None:
            raise ValueError("Must provide Gml or Geometry for Locatie")
        return v


class Werkingsgebied(BaseModel):
    UUID: uuid.UUID
    Code: str
    New: bool
    Frbr: GioFRBR
    Title: str
    Symbol: str
    Achtergrond_Verwijzing: str
    Achtergrond_Actualiteit: str
    Locaties: List[Locatie] = Field(..., alias="Onderverdelingen")

    def get_name(self) -> str:
        s: str = self.Title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_name()}.gml"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_name()}.xml"
