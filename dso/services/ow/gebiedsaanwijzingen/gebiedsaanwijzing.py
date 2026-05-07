from typing import Dict, List, Optional

from dso.services.ow.gebiedsaanwijzingen.gen import GA_OMGEVINGSVISIE_DATA, GA_PROGRAMMA_DATA
from dso.services.ow.gebiedsaanwijzingen.types import Gebiedsaanwijzing
from ....services.koop.waardelijsten.gen import TyperingVanRegelingen


class Gebiedsaanwijzingen:
    def __init__(self, document_type: TyperingVanRegelingen, data: List[Gebiedsaanwijzing]):
        self._document_type: TyperingVanRegelingen = document_type
        self._data: List[Gebiedsaanwijzing] = data

    def get_document_type(self) -> TyperingVanRegelingen:
        return self._document_type

    def get_by_type_label(self, label: str) -> Optional[Gebiedsaanwijzing]:
        for aanwijzing in self._data:
            if aanwijzing.aanwijzing_type.label == label:
                return aanwijzing

        return None

    def get_list(self) -> List[Gebiedsaanwijzing]:
        return self._data


# Service to use the Gebiedsaanwijzingen Waardelijsten
class GebiedsaanwijzingenFactory:
    def __init__(self):
        self._data: Dict[TyperingVanRegelingen, Gebiedsaanwijzingen] = {
            g.get_document_type(): g
            for g in [
                Gebiedsaanwijzingen(TyperingVanRegelingen.omgevingsvisie, GA_OMGEVINGSVISIE_DATA),
                Gebiedsaanwijzingen(TyperingVanRegelingen.programma, GA_PROGRAMMA_DATA),
            ]
        }

    def get_for_document(self, document_type: TyperingVanRegelingen) -> Optional[Gebiedsaanwijzingen]:
        return self._data.get(document_type)
