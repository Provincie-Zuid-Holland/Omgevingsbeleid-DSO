from pydantic import BaseModel
from typing import List, Optional, Union

class CodeEntry(BaseModel):
    id: str
    content: str

class Symboolcode(BaseModel):
    lijn: Optional[CodeEntry]
    punt: Optional[CodeEntry]
    vlak: Optional[CodeEntry]

class ValueEntry(BaseModel):
    label: str
    term: str
    uri: str
    definitie: str
    toelichting: str
    bron: str
    domein: str
    specialisatie: str
    symboolcode: Optional[Union[str, Symboolcode]] = None

class Waarden(BaseModel):
    waarde: List[ValueEntry]

class ValueList(BaseModel):
    label: str
    titel: str
    uri: str
    type: str
    omschrijving: str
    toelichting: str
    version: Optional[str] = None
    waarden: Waarden

class Waardelijsten(BaseModel):
    versie: str
    set: str
    waardelijst: List[ValueList]

class WaardelijstenRoot(BaseModel):
    waardelijsten: Waardelijsten
