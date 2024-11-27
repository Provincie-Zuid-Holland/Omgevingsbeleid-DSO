import uuid

from pydantic import BaseModel

from ......models import GioFRBR


class ActAttachment(BaseModel):
    UUID: uuid.UUID
    Code: str
    Frbr: GioFRBR
    New: bool
    Filename: str
    Title: str
    Geboorteregeling: str
    Content_Type: str
    Binary: bytes
    Hierarchy_Code: str

    def get_filename(self) -> str:
        return self.Filename

    def get_io_filename(self) -> str:
        filename: str = f"io_{self.Filename.replace('.', '_')}.xml"
        return filename
