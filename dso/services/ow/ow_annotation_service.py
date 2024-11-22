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

    {
    "beleidskeuze-756": [
        {
            "type_annotation": "gebied",
            "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7",
            "object_code": "beleidskeuze-756",
            "gebied_code": "werkingsgebied-28",
            ...
        },
        {
            "type_annotation": "thema",
            "wid": "...",
            "thema_waardes": ["bodem", "geluid"],
            ...
        }
    ]
}

    annotation types handled:
        - gebied
        - ambtsgebied
        - gebiedsaanwijzing
        - thema
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
        data_hinted_elements = xml_root.xpath("//* [attribute::*[starts-with(name(), 'data-hint-')]]")
        
        for element in data_hinted_elements:
            if element.tag == "Divisietekst":
                object_code = element.get("data-hint-object-code")
                
                if object_code not in self._annotation_map:
                    self._annotation_map[object_code] = []
                
                if element.get("data-hint-gebied-code") or element.get("data-hint-ambtsgebied"):
                    self._add_gebied_annotation(element)
                
                if element.get("data-hint-themas"):
                    self._add_thema_annotation(element)
                    
                if element.get("data-hint-hoofdlijnen"):
                    self._add_hoofdlijn_annotation(element)
                    
            if element.tag == "IntIoRef":
                self._add_gebiedsaanwijzing_annotation(element)

    def _add_gebied_annotation(self, element) -> None:
        """Handle gebied/ambtsgebied annotation"""
        try:
            object_code = element.get("data-hint-object-code")
            wid = element.get("wId")
        except KeyError:
            raise ValueError("Creating gebied annotation without data-hint-object-code or wId.")

        gebied_code = element.get("data-hint-gebied-code", None)
        uses_ambtsgebied: bool = element.get("data-hint-ambtsgebied", False)

        if uses_ambtsgebied:
            annotation = {
                "type_annotation": "ambtsgebied",
                "wid": wid,
                "tag": element.tag,
                "object_code": object_code,
            }
        elif gebied_code:
            werkingsgebied = self._werkingsgebied_repository.get_by_code(gebied_code)
            annotation = {
                "type_annotation": "gebied",
                "wid": wid,
                "tag": element.tag,
                "object_code": object_code,
                "gebied_code": gebied_code,
                "gio_ref": werkingsgebied.Identifier,
            }
        
        self._annotation_map[object_code].append(annotation)

    def _add_thema_annotation(self, element) -> None:
        """Handle thema annotation"""
        try:
            object_code = element.get("data-hint-object-code")
            wid = element.get("wId")
        except KeyError:
            raise ValueError("Creating thema annotation without data-hint-object-code or wId.")

        thema_waardes = [theme.strip() for theme in element.get("data-hint-themas").split(",")]

        #TODO: validate in registry?
        
        annotation = {
            "type_annotation": "thema",
            "wid": wid,
            "object_code": object_code,
            "thema_waardes": thema_waardes
        }
        
        self._annotation_map[object_code].append(annotation)

    def _add_gebiedsaanwijzing_annotation(self, element) -> None:
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
        gba_groep = element.get("data-hint-gebiedengroep", None)
        gba_type = element.get("data-hint-gebiedsaanwijzingtype", None)

        if not all([gba_locatie, gba_type, gba_groep]):
            raise ValueError("Missing data-hint-* attributes for gebiedsaanwijzing")

        # retrieve the used inioref pointers WID from bijlage
        wid_ref_key_pattern = f"bijlage-werkingsgebieden-divisietekst-referentie-{gba_locatie}-ref"
        for key, value in self._state_used_wid_map.items():
            if re.match(wid_ref_key_pattern, key):
                # replace the element "ref" tag  with annotation_ref_wid
                element.attrib["ref"] = value
                break

        annotation = {
            "type_annotation": "gebiedsaanwijzing",
            "ref": element.get("ref"),
            "wid": element.get("wId"),
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
        
        self._annotation_map[div_object_code].append(annotation)

    def _add_hoofdlijn_annotation(self, element) -> None:
        try:
            object_code = element.get("data-hint-object-code")
            wid = element.get("wId")
        except KeyError:
            raise ValueError("Creating hoofdlijn annotation without data-hint-object-code or wId.")

        hoofdlijnen = []
        for hoofdlijn_str in element.get("data-hint-hoofdlijnen").split(","):
            soort, naam = hoofdlijn_str.split("|", 1)
            hoofdlijnen.append({
                "soort": soort.strip(),
                "naam": naam.strip()
            })

        annotation = {
            "type_annotation": "hoofdlijn",
            "wid": wid,
            "object_code": object_code,
            "hoofdlijnen": hoofdlijnen
        }
        
        self._annotation_map[object_code].append(annotation)
