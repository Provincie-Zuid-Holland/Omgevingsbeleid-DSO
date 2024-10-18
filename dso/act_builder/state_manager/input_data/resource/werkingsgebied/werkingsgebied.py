import re
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, root_validator, validator

from ......models import GioFRBR


class Locatie(BaseModel):
    UUID: uuid.UUID
    Identifier: str
    Title: str
    Gml: Optional[str] = Field(None)
    Geometry: Optional[str] = Field(None)

    @root_validator
    def _must_have_a_source(cls, v):
        if v["Gml"] is None and v["Geometry"] is None:
            raise ValueError("Must provide Gml or Geometry for Locatie")
        return v


class Werkingsgebied(BaseModel):
    UUID: uuid.UUID
    Identifier: str
    Code: str
    New: bool
    Frbr: GioFRBR
    Title: str
    Geboorteregeling: str
    Achtergrond_Verwijzing: str
    Achtergrond_Actualiteit: str
    Locaties: List[Locatie] = Field(default_factory=list, alias="Onderverdelingen")

    @validator("Locaties", pre=True, always=True)
    def handle_locaties_alias(cls, v, values, **kwargs):
        if not v and "Onderverdelingen" in values:
            return values["Onderverdelingen"]
        return v

    def get_name(self) -> str:
        s: str = self.Title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_name()}.gml"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_name()}.xml"

    class Config:
        allow_population_by_field_name = True
        json_encoders = {uuid.UUID: str}
