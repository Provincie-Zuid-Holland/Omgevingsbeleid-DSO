from typing import Dict, List, Optional

from .besluit_pdf import BesluitPdf


class BesluitPdfRepository:
    def __init__(self):
        self._pdfs: Dict[str, BesluitPdf] = {}

    def add(self, pdf: dict):
        pdf_id = pdf["id"]
        self._pdfs[pdf_id] = BesluitPdf.parse_obj(pdf)

    def add_list(self, pdfs: List[dict]):
        for pdf in pdfs:
            self.add(pdf)

    def get_optional(self, idx: int) -> Optional[BesluitPdf]:
        pdf: Optional[BesluitPdf] = self._pdfs.get(idx)
        return pdf

    def get(self, idx: int) -> BesluitPdf:
        pdf: Optional[BesluitPdf] = self.get_optional(idx)
        if pdf is None:
            raise RuntimeError(f"Can not find pdf {idx}")
        return pdf

    def all(self) -> List[BesluitPdf]:
        return list(self._pdfs.values())

    def is_empty(self) -> bool:
        return not self._pdfs

    def to_dict(self) -> Dict[str, str]:
        serializable_data = {str(k): v.get_filename() for k, v in self._pdfs.items()}
        return serializable_data
