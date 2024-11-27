import uuid

from pydantic import BaseModel

from ......models import GioFRBR


class ActAttachment(BaseModel):
    uuid: uuid.UUID
    filename: str
    title: str
    binary: bytes
    content_type: str
    frbr: GioFRBR

    def get_filename(self) -> str:
        return self.filename

    def get_io_filename(self) -> str:
        filename: str = f"io_{self.filename.replace('.', '_')}.xml"
        return filename
