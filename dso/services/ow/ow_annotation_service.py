from collections import defaultdict
from typing import Dict, List, Union

from bs4 import BeautifulSoup

from ...act_builder.state_manager.input_data.resource.policy_object.policy_object_repository import (
    PolicyObjectRepository,
)
from ...act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from .annotation_models import (
    AmbtsgebiedAnnotation,
    GebiedAnnotation,
    GebiedsaanwijzingAnnotation,
    HoofdlijnAnnotation,
    ParentDiv,
    ThemaAnnotation,
)

AnnotationType = Union[
    GebiedAnnotation,
    AmbtsgebiedAnnotation,
    GebiedsaanwijzingAnnotation,
    ThemaAnnotation,
    HoofdlijnAnnotation,
]


class OWAnnotationService:
    def __init__(
        self,
        werkingsgebied_repository: WerkingsgebiedRepository,
        policy_object_repository: PolicyObjectRepository,
        used_wid_map: Dict[str, str] = {},
    ):
        self._werkingsgebied_repository = werkingsgebied_repository
        self._policy_object_repository = policy_object_repository
        self._state_used_wid_map = used_wid_map
        self._annotation_map: Dict[str, List[AnnotationType]] = defaultdict(list)

    def get_annotation_map(self) -> Dict[str, List[AnnotationType]]:
        return self._annotation_map

    def build_annotation_map(self) -> Dict[str, List[AnnotationType]]:
        """Build annotation map from policy objects instead of XML"""
        for object_code, policy_object in self._policy_object_repository._data.items():
            policy_dict = policy_object.to_dict()

            if "Werkingsgebied_Code" in policy_dict:
                self._add_gebied_annotation(policy_dict, object_code)

            if policy_dict.get("Themas"):
                self._add_thema_annotation(policy_dict, object_code)

            if policy_dict.get("Hoofdlijnen"):
                self._add_hoofdlijn_annotations(policy_dict, object_code)

            if policy_dict.get("Description"):
                self._add_gebiedsaanwijzing_annotations(policy_dict, object_code)

        return self._annotation_map

    def _add_gebied_annotation(self, policy_dict: dict, object_code: str) -> None:
        """Handle gebied/ambtsgebied annotation from policy object"""
        gebied_code = policy_dict.get("Werkingsgebied_Code")
        wid = self._state_used_wid_map.get(object_code)

        if gebied_code is None:
            annotation = AmbtsgebiedAnnotation(
                wid=wid,
                tag="Divisietekst",
                object_code=object_code,
            )
        else:
            werkingsgebied = self._werkingsgebied_repository.get_by_code(gebied_code)
            annotation = GebiedAnnotation(
                wid=wid,
                tag="Divisietekst",
                object_code=object_code,
                gebied_code=gebied_code,
                gio_ref=werkingsgebied.Identifier,
            )

        self._annotation_map[object_code].append(annotation)

    def _add_thema_annotation(self, policy_dict: dict, object_code: str) -> None:
        """Handle thema annotation from policy object"""
        annotation = ThemaAnnotation(
            tag="Divisietekst",
            wid=self._state_used_wid_map.get(object_code),
            object_code=object_code,
            thema_waardes=policy_dict["Themas"],
        )

        self._annotation_map[object_code].append(annotation)

    def _add_hoofdlijn_annotations(self, policy_dict: dict, object_code: str) -> None:
        """Handle hoofdlijn annotation from policy object"""
        for hoofdlijn in policy_dict["Hoofdlijnen"]:
            annotation = HoofdlijnAnnotation(
                tag="Divisietekst",
                wid=self._state_used_wid_map.get(object_code),
                object_code=object_code,
                soort=hoofdlijn["soort"],
                naam=hoofdlijn["naam"],
            )
            self._annotation_map[object_code].append(annotation)

    def _add_gebiedsaanwijzing_annotations(self, policy_dict: dict, object_code: str) -> None:
        """Extract and handle gebiedsaanwijzing annotations from Description HTML"""
        soup = BeautifulSoup(policy_dict["Description"], "html.parser")
        parent_wid = self._state_used_wid_map.get(object_code)

        gba_list = soup.find_all("a", attrs={"data-hint-type": "gebiedsaanwijzing"})

        for idx, a_tag in enumerate(gba_list, start=1):
            locatie = a_tag["data-hint-locatie"]
            gba_wid = self._state_used_wid_map.get(f"{object_code}-gebiedsaanwijzing-{idx}")

            parent_div = ParentDiv(
                wid=parent_wid,
                **{
                    "object-code": object_code,
                    "gebied-code": policy_dict.get("Werkingsgebied_Code"),
                    "uses_ambtsgebied": policy_dict.get("Werkingsgebied_Code") is None,
                },
            )

            annotation = GebiedsaanwijzingAnnotation(
                tag="IntIoRef",
                wid=gba_wid,
                werkingsgebied_code=locatie,
                groep=a_tag["data-hint-gebiedengroep"],
                type=a_tag["data-hint-gebiedsaanwijzingtype"],
                parent_div=parent_div,
                object_code=object_code,
            )

            self._annotation_map[object_code].append(annotation)
