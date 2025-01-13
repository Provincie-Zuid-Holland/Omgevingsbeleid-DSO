from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ParentDiv(BaseModel):
    wid: str
    object_code: str = Field(alias="object-code")
    gebied_code: Optional[str] = Field(alias="gebied-code")
    uses_ambtsgebied: bool

    class Config:
        allow_population_by_field_name = True


class BaseAnnotation(BaseModel):
    tag: str
    wid: str
    object_code: str


class GebiedAnnotation(BaseAnnotation):
    gebied_code: str
    gio_ref: str


class AmbtsgebiedAnnotation(BaseAnnotation):
    pass


class GebiedsaanwijzingAnnotation(BaseAnnotation):
    werkingsgebied_code: str
    groep: str
    type: str
    parent_div: ParentDiv


class ThemaAnnotation(BaseAnnotation):
    thema_waardes: List[str]


class HoofdlijnAnnotation(BaseAnnotation):
    soort: str
    naam: str
