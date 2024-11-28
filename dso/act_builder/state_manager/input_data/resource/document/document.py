import uuid

from pydantic import BaseModel, validator

from ......models import ContentType, GioFRBR


class Document(BaseModel):
    UUID: uuid.UUID
    Code: str
    Frbr: GioFRBR
    New: bool
    Filename: str
    Title: str
    Geboorteregeling: str
    Content_Type: ContentType
    Binary: bytes
    Hierarchy_Code: str

    def get_filename(self) -> str:
        return self.Filename

    def get_io_filename(self) -> str:
        filename: str = f"io_{self.Filename.replace('.', '_')}.xml"
        return filename

    @validator("Content_Type", pre=True, always=True)
    def _format_content_type(cls, v):
        if v in ContentType.__members__.values():
            return v
        return ContentType[v]
