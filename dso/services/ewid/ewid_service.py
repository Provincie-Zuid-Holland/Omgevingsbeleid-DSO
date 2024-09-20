import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, List, Optional

from ...act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ...act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from . import ELEMENT_REF, EIDGenerationError


class EWIDService:
    """
    The EWIDService class is responsible for generating EWID for policy objects.
    """

    def __init__(
        self,
        wid_prefix: str,
        known_wid_map: Dict[str, str] = {},
        known_wids: List[str] = [],
        werkingsgebied_repository: Optional[WerkingsgebiedRepository] = None,
    ):
        self._werkingsgebied_repository: Optional[WerkingsgebiedRepository] = werkingsgebied_repository
        self._wid_prefix: str = wid_prefix
        self._known_wid_map: Dict[str, str] = known_wid_map
        # Make it a map for faster lookup
        self._known_wids: Dict[str, bool] = {wid: True for wid in known_wids}

        self._element_refs: Dict[str, str] = ELEMENT_REF
        self._eid_counters = defaultdict(lambda: defaultdict(int))
        self._wid_counters = defaultdict(lambda: defaultdict(int))

        # wId's used by indentifiers, for example beleidskeuze-4 by that object
        # Although it should be possible to add custom identifiers
        self._state_used_wid_map: Dict[str, str] = {}
        # All used wids, for export purposes
        # This will be send in the input data for the next version of this Act
        self._state_used_wids: List[str] = []

        # wId lookup used by OW files
        self._state_object_tekst_lookup: dict = {}

    def add_ewids(self, xml_source: str, parent_eid="", parent_wid="", parent_tag_name="") -> str:
        root = self._parse_xml(xml_source)
        self._fill_ewid(root, parent_eid, parent_wid, parent_tag_name)
        result_xml: str = ET.tostring(root, encoding="utf-8").decode("utf-8")
        return result_xml

    def get_state_used_wid_map(self) -> Dict[str, str]:
        return self._state_used_wid_map

    def get_state_used_wids(self) -> List[str]:
        return self._state_used_wids

    def get_state_object_tekst_lookup(self) -> dict:
        return self._state_object_tekst_lookup

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

        # By default, we will generate a new wId based on the eId
        # Then we might override the wId if we think that a previous Act Version already generated it
        wid = f"{self._wid_prefix}__{eid}"

        wid_lookup_object_code = element.get("data-hint-wid-code", None)
        if wid_lookup_object_code:
            # This will force to use a specific wId because we are really certain
            # Like for our api objects
            if wid_lookup_object_code in self._known_wid_map:
                wid = self._known_wid_map[wid_lookup_object_code]

            # If you are forced (via data-wid-code) and we are in a Divisietekst
            # Then we pretty much sure that it
            if tag_name in ["Divisietekst"]:
                parent_wid = wid if tag_name in self._element_refs else ""
        elif parent_wid != "":
            potential_wid: str = self._generate_wid(tag_name, parent_wid, parent_tag_name)
            # This is mosly the result of parents being forced to a wId (parents matched the previous if)
            # Now we would like to continue on our parents (previous act version) path.
            # But we can only do so, if the wId was actually created in previous Act
            if self._known_wids.get(potential_wid, False):
                # The wid from another act version is valid
                wid = potential_wid
                if tag_name in self._element_refs:
                    parent_wid = wid

        if tag_name in self._element_refs:
            self._state_used_wids.append(wid)
            element.set("eId", eid)
            element.set("wId", wid)

        if wid_lookup_object_code is not None:
            self._state_used_wid_map[wid_lookup_object_code] = wid

        if self._werkingsgebied_repository is not None:
            # Remember the EWID for location annotated policy objects
            object_code = element.get("data-hint-object-code", None)
            gebied_code = element.get("data-hint-gebied-code", None)
            uses_ambtsgebied: bool = element.get("data-hint-ambtsgebied", False)

            if object_code is not None and uses_ambtsgebied:
                self._state_object_tekst_lookup[object_code] = {
                    "wid": wid,
                    "tag": element.tag,
                    "object_code": object_code,
                    "uses_ambtsgebied": True,
                }
            elif object_code is not None and gebied_code is not None:
                werkingsgebied: Werkingsgebied = self._werkingsgebied_repository.get_by_code(gebied_code)
                self._state_object_tekst_lookup[object_code] = {
                    "wid": wid,
                    "tag": element.tag,
                    "object_code": object_code,
                    "gebied_code": gebied_code,
                    "gebied_uuid": str(werkingsgebied.UUID),
                    "uses_ambtsgebied": False,
                }

        for child in element:
            self._fill_ewid(
                child,
                child_parent_eid,
                parent_wid,
                tag_name,
            )
