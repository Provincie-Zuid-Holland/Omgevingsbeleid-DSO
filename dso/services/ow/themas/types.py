from pydantic import BaseModel


class Thema(BaseModel):
    label: str
    term: str
    uri: str
    definitie: str
    toelichting: str
    bron: str
    domein: str
    deprecated: bool
