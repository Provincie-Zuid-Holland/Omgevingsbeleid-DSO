import uuid

from pydantic import BaseModel


class Hoofdlijn(BaseModel):
    UUID: uuid.UUID
    Code: str
    Title: str
    Hoofdlijn_Type: str

    def get_title(self) -> str:
        return self.Title
