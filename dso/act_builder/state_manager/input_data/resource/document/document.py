import uuid

from pydantic import BaseModel, field_validator

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

    def get_filename(self) -> str:
        return self.Filename

    def get_io_filename(self) -> str:
        filename: str = f"IO_{self.Filename.replace('.', '_')}.xml"
        return filename

    @field_validator("Content_Type", mode="before")
    def _format_content_type(cls, value):
        if value in ContentType.__members__.values():
            return value
        return ContentType[value]
