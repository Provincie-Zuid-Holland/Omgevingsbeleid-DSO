import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, Optional

from ...builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ...builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from ...builder.state_manager.state_manager import StateManager
from . import ELEMENT_REF, EIDGenerationError


class EWIDService:
    """
    The EWIDService class is responsible for generating EWID for policy objects.
    """

    def __init__(
        self,
        state_manager: Optional[StateManager],
        wid_prefix: str,
        known_wid_map: Dict[str, str] = {},
    ):
        self._wid_prefix = wid_prefix
        self._known_wid_map: Dict[str, str] = known_wid_map

        self._state_manager: Optional[StateManager] = state_manager
        self._werkingsgebied_repository: Optional[WerkingsgebiedRepository] = None
        if state_manager is not None:
            self._werkingsgebied_repository = state_manager.input_data.resources.werkingsgebied_repository

        self._element_refs: Dict[str, str] = {e.name: e.value for e in ELEMENT_REF}
        self._eid_counters = defaultdict(lambda: defaultdict(int))
        self._wid_counters = defaultdict(lambda: defaultdict(int))

    def add_ewids(self, xml_source: str) -> str:
        root = self._parse_xml(xml_source)
        self._fill_ewid(root)
        result_xml: str = ET.tostring(root, encoding="utf-8")
        return result_xml

    def _parse_xml(self, xml_string: str):
        try:
            tree = ET.ElementTree(ET.fromstring(xml_string))
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise EIDGenerationError(xml_string, str(e))

    def _generate_eid(self, tag_name: str, parent_eid: str, parent_tag_name: str) -> str:
        eid_value = self._element_refs.get(tag_name, tag_name)
        parent_key = parent_eid if parent_eid else parent_tag_name

        self._eid_counters[parent_key][eid_value] += 1
        count: int = self._eid_counters[parent_key][eid_value]

        new_eid = f"{eid_value}_o_{count}"
        return f"{parent_eid}__{new_eid}" if parent_eid else new_eid

    def _generate_wid(self, tag_name: str, parent_wid: str, parent_tag_name: str) -> str:
        wid_value = self._element_refs.get(tag_name, tag_name)
        parent_key = parent_wid if parent_wid else parent_tag_name

        self._wid_counters[parent_key][wid_value] += 1
        count: int = self._wid_counters[parent_key][wid_value]

        new_wid = f"{wid_value}_o_{count}"
        return f"{parent_wid}__{new_wid}"

    def _fill_ewid(self, element, parent_eid="", parent_wid="", parent_tag_name=""):
        """
        Fills the EWID for the given element and its children.
        """
        tag_name = element.tag
        eid = self._generate_eid(tag_name, parent_eid, parent_tag_name)
        child_parent_eid = eid if tag_name in self._element_refs else parent_eid

        wid_lookup_object_code = element.get("data-hint-wid-code", None)
        if wid_lookup_object_code in self._known_wid_map:
            wid = self._known_wid_map[wid_lookup_object_code]
            child_parent_wid = wid if tag_name in self._element_refs else ""
        elif parent_wid != "":
            wid = self._generate_wid(tag_name, parent_wid, parent_tag_name)
            child_parent_wid = wid if tag_name in self._element_refs else ""
        else:
            wid = f"{self._wid_prefix}__{eid}"
            child_parent_wid = ""

        if tag_name in self._element_refs:
            element.set("eId", eid)
            element.set("wId", wid)

        if self._state_manager is not None:
            object_code = element.get("data-hint-object-code", None)
            gebied_code = element.get("data-hint-gebied-code", None)

            # Remember the WID for policy objects
            if object_code is not None:
                self._state_manager.used_wid_map[object_code] = wid

            # Remember the EWID for location annotated policy objects
            if object_code is not None and gebied_code is not None:
                werkingsgebied: Werkingsgebied = self._werkingsgebied_repository.get_by_code(gebied_code)
                self._state_manager.object_tekst_lookup[object_code] = {
                    "wid": wid,
                    "tag": element.tag,
                    "gebied_code": gebied_code,
                    "gebied_uuid": str(werkingsgebied.UUID),
                }

        for child in element:
            self._fill_ewid(
                child,
                child_parent_eid,
                child_parent_wid,
                tag_name,
            )
