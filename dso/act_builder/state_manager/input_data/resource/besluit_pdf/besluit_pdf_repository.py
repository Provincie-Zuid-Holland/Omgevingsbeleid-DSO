from .besluit_pdf import BesluitPdf


class BesluitPdfRepository:
    def __init__(self):
        self._pdfs: dict[str, BesluitPdf] = {}

    def add(self, pdf: dict):
        pdf_id = pdf["id"]
        self._pdfs[pdf_id] = BesluitPdf.model_validate(pdf)

    def add_list(self, pdfs: list[dict]):
        for pdf in pdfs:
            self.add(pdf)

    def get_optional(self, idx: int) -> BesluitPdf | None:
        pdf: BesluitPdf | None = self._pdfs.get(idx)
        return pdf

    def get(self, idx: int) -> BesluitPdf:
        pdf: BesluitPdf | None = self.get_optional(idx)
        if pdf is None:
            raise RuntimeError(f"Can not find pdf {idx}")
        return pdf

    def all(self) -> list[BesluitPdf]:
        return list(self._pdfs.values())

    def is_empty(self) -> bool:
        return not self._pdfs

    def to_dict(self) -> dict[str, str]:
        serializable_data = {str(k): v.get_filename() for k, v in self._pdfs.items()}
        return serializable_data
