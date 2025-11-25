from typing import Dict, List, Optional
from dso.models import DocumentType
from dso.services.ow.area_designation.gen import GA_OMGEVINGSVISIE_DATA, GA_PROGRAMMA_DATA
from dso.services.ow.area_designation.types import AreaDesignation


class AreaDesignations:
    def __init__(self, document_type: DocumentType, data: List[AreaDesignation]):
        self._document_type: DocumentType = document_type
        self._data: List[AreaDesignation] = data

    def get_document_type(self) -> DocumentType:
        return self._document_type

    def get_by_type_label(self, label: str) -> Optional[AreaDesignation]:
        for designation in self._data:
            if designation.designation_type.label == label:
                return designation

        return None


# Service to use the Gebiedsaanwijzingen Waardelijsten
class AreaDesignationsFactory:
    def __init__(self):
        self._data: Dict[DocumentType, AreaDesignations] = {
            g.get_document_type(): g
            for g in [
                AreaDesignations(DocumentType.OMGEVINGSVISIE, GA_OMGEVINGSVISIE_DATA),
                AreaDesignations(DocumentType.PROGRAMMA, GA_PROGRAMMA_DATA),
            ]
        }

    def get_for_document(self, document_type: DocumentType) -> Optional[AreaDesignations]:
        return self._data.get(document_type)
