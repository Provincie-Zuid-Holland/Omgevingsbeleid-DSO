import uuid

from pydantic import BaseModel

from ......models import PubdataFRBR


class Pdf(BaseModel):
    id: int
    uuid: uuid.UUID
    filename: str
    title: str
    binary: bytes
    frbr: PubdataFRBR

    def get_filename(self) -> str:
        filename: str = f"pdf_{self.filename}"
        return filename

    def get_io_filename(self) -> str:
        filename: str = f"io_pdf_{self.filename}.xml"
        return filename
