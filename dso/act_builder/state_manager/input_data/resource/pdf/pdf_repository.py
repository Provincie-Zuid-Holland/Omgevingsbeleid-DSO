from typing import Dict, List, Optional

from .pdf import Pdf


class PdfRepository:
    def __init__(self):
        self._pdfs: Dict[str, Pdf] = {}

    def add(self, pdf: dict):
        pdf_id = pdf["id"]
        self._pdfs[pdf_id] = Pdf.parse_obj(pdf)

    def add_list(self, pdfs: List[dict]):
        for pdf in pdfs:
            self.add(pdf)

    def get_optional(self, idx: int) -> Optional[Pdf]:
        pdf: Optional[Pdf] = self._pdfs.get(idx)
        return pdf

    def get(self, idx: int) -> Pdf:
        pdf: Optional[Pdf] = self.get_optional(idx)
        if pdf is None:
            raise RuntimeError(f"Can not find pdf {idx}")
        return pdf

    def all(self) -> List[Pdf]:
        return list(self._pdfs.values())

    def is_empty(self) -> bool:
        return not self._pdfs
