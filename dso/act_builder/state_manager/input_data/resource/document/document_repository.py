from typing import Dict, List, Optional

from .document import Document


class DocumentRepository:
    def __init__(self):
        self._documents: Dict[str, Document] = {}

    def add(self, document: dict):
        uuidx: str = document["UUID"]
        self._documents[uuidx] = Document.parse_obj(document)

    def add_list(self, documents: List[dict]):
        for document in documents:
            self.add(document)

    def get_optional(self, uuidx: str) -> Optional[Document]:
        result: Optional[Document] = self._documents.get(uuidx)
        return result

    def get(self, uuidx: str) -> Document:
        result: Optional[Document] = self.get_optional(uuidx)
        if result is None:
            raise RuntimeError(f"Can not find document with uuid `{uuidx}`")
        return result

    def all(self) -> List[Document]:
        return list(self._documents.values())

    def is_empty(self) -> bool:
        return not self._documents

    def to_dict(self) -> Dict[str, str]:
        serializable_data = {str(k): v.get_filename() for k, v in self._documents.items()}
        return serializable_data

    def get_by_codes(self, codes: List[str]) -> List[Document]:
        result: List[Document] = [d for _, d in self._documents.items() if d.Code in codes]
        return result
