import re
import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator

from ......models import GioFRBR


class Locatie(BaseModel):
    UUID: uuid.UUID
    Identifier: str
    Gml_ID: str
    Group_ID: str
    Title: str
    Gml: Optional[str] = Field(None)
    Geometry: Optional[str] = Field(None)

    @model_validator(mode="after")
    def _must_have_a_source(self) -> Self:
        if self.Gml is None and self.Geometry is None:
            raise ValueError("Must provide Gml or Geometry for Locatie")
        return self


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

    @field_validator("Locaties", mode="before")
    def handle_locaties_alias(cls, v, info):
        if not v and "Onderverdelingen" in info.data:
            return info.data["Onderverdelingen"]
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

    @field_serializer("UUID")
    def serialize_uuid(cls, v: uuid.UUID) -> str:
        return str(v)

    model_config = ConfigDict(populate_by_name=True)
