import re
from typing import Dict

from lxml import etree

from ...act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)


class OWAnnotationService:
    """
    Service to build OW annotations from STOP XML data-hints
    result is a dict map of annotation info per STOP wid item.

    This annotation map is consumed by OW builder classes as
    input for change comparison.

    e.g.

    "beleidskeuze-756": {
        "type_annotation": "gebied",
        "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7",
        "tag": "Divisietekst",
        "object_code": "beleidskeuze-756",
        "gebied_code": "werkingsgebied-28",
        "gebied_uuid": "6cee5d12-beaa-4ea8-9464-5697a6e85931",
        "uses_ambtsgebied": False,
    },

    annotation types handled:
        - gebied
        - ambtsgebied
        - gebiedsaanwijzing
    """

    def __init__(
        self,
        werkingsgebied_repository: WerkingsgebiedRepository,
        used_wid_map: Dict[str, str] = {},
    ):
        self._werkingsgebied_repository: WerkingsgebiedRepository = werkingsgebied_repository
        self._state_used_wid_map: Dict[str, str] = used_wid_map
        self._annotation_map: dict = {}

    def get_annotation_map(self) -> Dict[str, str]:
        return self._annotation_map

    def build_annotation_map(self, xml_source: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_source.encode("utf-8"), parser)

        self._parse_data_hints(xml_root=root)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _parse_data_hints(self, xml_root) -> None:
        """Build a map of OW annotations from STOP XML data-hints"""

        # find every element with a data-hint-* attribute and get its value
        # data_hinted_elements = xml_root.xpath("//Divisietekst[attribute::*[starts-with(name(), 'data-hint-')]]")
        data_hinted_elements = xml_root.xpath("//* [attribute::*[starts-with(name(), 'data-hint-')]]")
        for element in data_hinted_elements:
            if element.tag == "Divisietekst":
                # if gebied_code or ambtsgebied hint attribute is present, add annotation
                if element.get("data-hint-gebied-code") or element.get("data-hint-ambtsgebied"):
                    self._add_gebied_annotation(element)
                # add other possible annotations here..
                # - thema
                # - hoofdlijn
            if element.tag == "IntIoRef":
                self._add_gebiedsaanwijzing_annotation(element)

            # Gebiedsaanwijzing annotation
        return

    def _add_gebied_annotation(self, element) -> None:
        """
        handle new annotation mapping for standard werkingsgebied
        annotation or ambtsgebied annotations
        """
        try:
            object_code = element.get("data-hint-object-code")
            wid = element.get("wId")
        except KeyError:
            raise ValueError("Creating gebied annotation without data-hint-object-code or wId.")

        gebied_code = element.get("data-hint-gebied-code", None)
        uses_ambtsgebied: bool = element.get("data-hint-ambtsgebied", False)

        if uses_ambtsgebied:  # Ambtsgebied annotation
            self._annotation_map[object_code] = {
                "type_annotation": "ambtsgebied",
                "wid": wid,
                "tag": element.tag,
                "object_code": object_code,
            }
        elif gebied_code:  # Normal gebied Annotation
            werkingsgebied = self._werkingsgebied_repository.get_by_code(gebied_code)
            self._annotation_map[object_code] = {
                "type_annotation": "gebied",
                "wid": wid,
                "tag": element.tag,
                "object_code": object_code,
                "gebied_code": gebied_code,
                "gebied_uuid": str(werkingsgebied.UUID),
            }

        return

    def _add_gebiedsaanwijzing_annotation(self, element):
        parent = element.getparent()

        while parent is not None and not parent.get("wId"):
            parent = parent.getparent()

        if parent is None or parent.tag != "Divisietekst":
            raise ValueError("Gebiedsaanwijzing currently only supported on Divisietekst elements.")

        # upper divisietekst attributes
        div_wid = parent.get("wId")
        div_object_code = parent.get("data-hint-object-code")
        div_gebied_code = parent.get("data-hint-gebied-code", None)
        div_ambtsgebied = bool(parent.get("data-hint-ambtsgebied", False))

        # gebiedsaanwijzing tag attributes
        gba_locatie = element.get("data-hint-locatie", None)
        gba_type = element.get("data-hint-gebiedengroep", None)
        gba_groep = element.get("data-hint-gebiedsaanwijzingtype", None)

        if not all([gba_locatie, gba_type, gba_groep]):
            raise ValueError("Missing data-hint-* attributes for gebiedsaanwijzing")

        # retrieve the used inioref pointers WID from bijlage
        wid_ref_key_pattern = f"bijlage-werkingsgebieden-divisietekst-referentie-{gba_locatie}-ref"
        for key, value in self._state_used_wid_map.items():
            if re.match(wid_ref_key_pattern, key):
                # replace the element "ref" tag  with annotation_ref_wid
                element.attrib["ref"] = value
                break

        self._annotation_map[element.get("wId")] = {
            "type_annotation": "gebiedsaanwijzing",
            "ref": element.get("ref"),
            "werkingsgebied_code": gba_locatie,
            "groep": gba_groep,
            "type": gba_type,
            "parent_div": {
                "wid": div_wid,
                "object-code": div_object_code,
                "gebied-code": div_gebied_code,
                "uses_ambtsgebied": div_ambtsgebied,
            },
        }

        return
