from typing import Dict, List, Optional
from dso.models import DocumentType
from dso.services.ow.gebiedsaanwijzing.gen import GA_OMGEVINGSVISIE_DATA, GA_PROGRAMMA_DATA
from dso.services.ow.gebiedsaanwijzing.types import Gebiedsaanwijzing


class Gebiedsaanwijzingen:
    def __init__(self, document_type: DocumentType, data: List[Gebiedsaanwijzing]):
        self._document_type: DocumentType = document_type
        self._data: List[Gebiedsaanwijzing] = data

    def get_document_type(self) -> DocumentType:
        return self._document_type

    def get_by_type_label(self, label: str) -> Optional[Gebiedsaanwijzing]:
        for gebiedsaanwijzing in self._data:
            if gebiedsaanwijzing.aanwijzing_type.label == label:
                return gebiedsaanwijzing

        return None


class GebiedsaanwijzingenFactory:
    def __init__(self):
        self._data: Dict[DocumentType, Gebiedsaanwijzingen] = {
            g.get_document_type(): g
            for g in [
                Gebiedsaanwijzingen(DocumentType.OMGEVINGSVISIE, GA_OMGEVINGSVISIE_DATA),
                Gebiedsaanwijzingen(DocumentType.PROGRAMMA, GA_PROGRAMMA_DATA),
            ]
        }

    def get_for_document(self, document_type: DocumentType) -> Optional[Gebiedsaanwijzingen]:
        return self._data.get(document_type)
