import re
from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ......models import GioFRBR


class Gebied(BaseModel):
    uuid: UUID
    code: str
    identifier: str
    new: bool
    title: str

    # GIO
    frbr: GioFRBR
    geboorteregeling: str
    achtergrond_verwijzing: str
    achtergrond_actualiteit: str

    gml_id: str
    gml: str

    def get_name(self) -> str:
        s: str = self.title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_name()}.gml"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_name()}.xml"


class GebiedenGroep(BaseModel):
    uuid: UUID
    identifier: str
    code: str
    new: bool
    title: str
    gebied_codes: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)
