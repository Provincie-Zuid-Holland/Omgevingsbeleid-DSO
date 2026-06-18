import uuid

from pydantic import BaseModel


class Hoofdlijn(BaseModel):
    UUID: uuid.UUID
    Code: str
    Title: str
    Hoofdlijn_Type: str

    def get_title(self) -> str:
        return self.Title

    def get_hoofdlijn_type(self) -> str:
        return self.Hoofdlijn_Type
