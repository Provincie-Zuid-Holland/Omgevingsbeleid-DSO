from typing import Dict, Generic, List, Optional, TypeVar

from .constants import RESTRICTED_TYPE_GEBIEDSAANWIJZING
from .generated.imow_gebiedsaanwijzing_groep_values import IMOW_GEBIEDSAANWIJZING_GROEP_ITEMS
from .generated.imow_thema_values import IMOW_THEMA_ITEMS
from .generated.imow_type_gebiedsaanwijzing_values import IMOW_TYPE_GEBIEDSAANWIJZING_ITEMS
from .imow_models import GebiedsaanwijzingGroepValue, ThemaValue, TypeGebiedsaanwijzingValue

T = TypeVar("T")


class IMOWValueRegistry(Generic[T]):
    def __init__(self, values: List[T], key_attr: str = "uri"):
        self._values = values
        self._values_by_uri: Dict[str, T] = {getattr(v, key_attr): v for v in values}
        self._values_by_term: Dict[str, T] = {getattr(v, "term"): v for v in values}

    def get_all(self) -> List[T]:
        return self._values

    def get_by_uri(self, uri: str) -> T | None:
        return self._values_by_uri.get(uri)

    def get_by_term(self, term: str) -> T | None:
        return self._values_by_term.get(term)

    def get_by_any(self, value: str) -> T | None:
        return self.get_by_uri(value) or self.get_by_term(value)

    def get_uris(self) -> List[str]:
        return list(self._values_by_uri.keys())

    def get_labels(self) -> List[str]:
        return [v.label for v in self._values]


class IMOWValueRepository:
    def __init__(
        self,
        themas: List[ThemaValue],
        type_gebiedsaanwijzingen: List[TypeGebiedsaanwijzingValue],
        gebiedsaanwijzing_groepen: List[GebiedsaanwijzingGroepValue],
    ):
        self._themas = IMOWValueRegistry(themas)
        self._type_gebiedsaanwijzingen = IMOWValueRegistry(type_gebiedsaanwijzingen)
        self._gebiedsaanwijzing_groepen = IMOWValueRegistry(gebiedsaanwijzing_groepen)

        # for gebiedsanwijzinggroepen create a dictionary with the groups by type
        self._groups_by_type: Dict[str, List[GebiedsaanwijzingGroepValue]] = {}
        for group in gebiedsaanwijzing_groepen:
            if group.type_gebiedsaanwijzing not in self._groups_by_type:
                self._groups_by_type[group.type_gebiedsaanwijzing] = []
            self._groups_by_type[group.type_gebiedsaanwijzing].append(group)

    def get_all_themas(self) -> List[ThemaValue]:
        return self._themas.get_all()

    def get_all_type_gebiedsaanwijzingen(self, document_type: str | None = None) -> List[TypeGebiedsaanwijzingValue]:
        if not document_type:
            return self._type_gebiedsaanwijzingen.get_all()

        restricted_types = RESTRICTED_TYPE_GEBIEDSAANWIJZING.get(document_type, [])
        return [
            item
            for item in self._type_gebiedsaanwijzingen.get_all()
            if not any(restricted in item.uri for restricted in restricted_types)
        ]

    def get_all_gebiedsaanwijzing_groepen(self) -> List[GebiedsaanwijzingGroepValue]:
        return self._gebiedsaanwijzing_groepen.get_all()

    def get_groups_for_type(self, type_value: str) -> List[GebiedsaanwijzingGroepValue]:
        type_gebiedsaanwijzing = self._type_gebiedsaanwijzingen.get_by_any(type_value)
        if not type_gebiedsaanwijzing:
            return []
        return self._groups_by_type.get(type_gebiedsaanwijzing.uri, [])

    def get_thema_uris(self) -> List[str]:
        return self._themas.get_uris()

    def get_type_gebiedsaanwijzing_uris(self) -> List[str]:
        return self._type_gebiedsaanwijzingen.get_uris()

    def get_gebiedsaanwijzing_groep_uris(self) -> List[str]:
        return self._gebiedsaanwijzing_groepen.get_uris()

    def get_thema_labels(self) -> List[str]:
        return self._themas.get_labels()

    def get_type_gebiedsaanwijzing_labels(self) -> List[str]:
        return self._type_gebiedsaanwijzingen.get_labels()

    def get_gebiedsaanwijzing_groep_labels(self) -> List[str]:
        return self._gebiedsaanwijzing_groepen.get_labels()

    def get_type_gebiedsaanwijzing_uri(self, value: str) -> Optional[str]:
        type_gebiedsaanwijzing = self._type_gebiedsaanwijzingen.get_by_any(value)
        return type_gebiedsaanwijzing.uri if type_gebiedsaanwijzing else None

    def get_gebiedsaanwijzing_groep_uri(self, value: str) -> Optional[str]:
        gebiedsaanwijzing_groep = self._gebiedsaanwijzing_groepen.get_by_any(value)
        return gebiedsaanwijzing_groep.uri if gebiedsaanwijzing_groep else None


# create the registry with all generated IMOW values
imow_value_repository = IMOWValueRepository(
    IMOW_THEMA_ITEMS, IMOW_TYPE_GEBIEDSAANWIJZING_ITEMS, IMOW_GEBIEDSAANWIJZING_GROEP_ITEMS
)
