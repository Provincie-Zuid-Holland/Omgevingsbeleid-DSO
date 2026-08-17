from .document import Document


class DocumentRepository:
    def __init__(self):
        self._documents: dict[str, Document] = {}

    def add(self, document: dict):
        uuidx: str = document["UUID"]
        self._documents[uuidx] = Document.model_validate(document)

    def add_list(self, documents: list[dict]):
        for document in documents:
            self.add(document)

    def get_optional(self, uuidx: str) -> Document | None:
        result: Document | None = self._documents.get(uuidx)
        return result

    def get(self, uuidx: str) -> Document:
        result: Document | None = self.get_optional(uuidx)
        if result is None:
            raise RuntimeError(f"Can not find document with uuid `{uuidx}`")
        return result

    def all(self) -> list[Document]:
        return list(self._documents.values())

    def is_empty(self) -> bool:
        return not self._documents

    def to_dict(self) -> dict[str, str]:
        serializable_data = {str(k): v.get_filename() for k, v in self._documents.items()}
        return serializable_data

    def get_by_codes(self, codes: list[str]) -> list[Document]:
        result: list[Document] = [d for _, d in self._documents.items() if d.Code in codes]
        return result

    def get_new(self) -> list[Document]:
        return [d for d in self._documents.values() if d.New]
