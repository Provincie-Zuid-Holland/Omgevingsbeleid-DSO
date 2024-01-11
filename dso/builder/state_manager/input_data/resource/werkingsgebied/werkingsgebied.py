import re
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ......models import FRBR


class Locatie(BaseModel):
    Object_ID: Optional[int] = Field(None)
    Object_Code: Optional[str] = Field(None)
    UUID: uuid.UUID
    Title: str
    Symbol: str
    Created_Date: datetime
    Modified_Date: datetime
    Geometry: str


class Werkingsgebied(BaseModel):
    Object_ID: Optional[int] = Field(None)
    Object_Code: Optional[str] = Field(None)
    UUID: uuid.UUID
    Title: str
    Symbol: str
    Created_Date: datetime
    Modified_Date: datetime
    Achtergrond_Verwijzing: str
    Achtergrond_Actualiteit: str
    Locaties: List[Locatie] = Field(..., alias="Onderverdelingen")

    # Provided by the system instead of the resource json
    provincie_id: str
    expression_taal: str

    def get_FRBR(self) -> FRBR:
        identifier: str = self.get_identifier()
        work_datum: str = f"{self.Created_Date.year}"
        work: str = f"/join/id/regdata/{self.provincie_id}/{work_datum}/{identifier}"

        version: str = self.get_version(self.expression_taal)
        expression: str = f"{work}/{version}"

        return FRBR(
            work=work,
            expression=expression,
        )

    def get_identifier(self) -> str:
        s: str = self.Title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_version(self, expression_taal: str) -> str:
        date_version: str = self.Modified_Date.strftime("%Y-%m-%d;%H%M")
        version: str = f"{expression_taal}@{date_version}"
        return version

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_identifier()}.gml"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_identifier()}.xml"
