import xml.etree.ElementTree as ET
from collections import defaultdict

from ...builder.state_manager.state_manager import StateManager
from . import ELEMENT_REF, EIDGenerationError


class EWIDService:
    """
    The EWIDService class is responsible for generating EWID for policy objects.
    """

    def __init__(self, state_manager: StateManager, wid_prefix: str):
        """
        Initializes an instance of the EWIDService class.

        Args:
            state_manager (StateManager): The state manager object.
            wid_prefix (str): The prefix for the generated EWID.
        """
        self._state_manager: StateManager = state_manager

        self.wid_prefix = wid_prefix
        self.global_counters = defaultdict(lambda: defaultdict(int))

        self.root = None
        self.tree = None

    def parse_xml(self, xml_string: str):
        """
        Parses an XML string and sets the root and tree attributes.

        Args:
            xml_string (str): The XML string to parse.
        """
        try:
            self.tree = ET.ElementTree(ET.fromstring(xml_string))
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise EIDGenerationError(xml_string, str(e))

    def parse_xml_file(self, xml_source):
        """
        Parses an XML file and sets the root and tree attributes.

        Args:
            xml_source: The XML file to parse.
        """
        try:
            self.tree = ET.parse(xml_source)
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            raise EIDGenerationError(xml_source, str(e))

    def increment_counter(self, parent_key, eid_value):
        """
        Increments the counter for the given parent key and EWID value.

        Args:
            parent_key: The parent key.
            eid_value: The EWID value.

        Returns:
            int: The incremented counter value.
        """
        self.global_counters[parent_key][eid_value] += 1
        return self.global_counters[parent_key][eid_value]

    def generate_eid(self, element, parent_eid, parent_tag):
        """
        Generates a unique EWID for the given element according
        to explicit structure.

        Args:
            element: The element for which to generate the EWID.
            parent_eid: The parent EWID.
            parent_tag: The parent tag.

        Returns:
            str: The generated EWID.
        """
        tag = element.tag
        eid_value = ELEMENT_REF[tag].value if tag in ELEMENT_REF.__members__ else tag
        parent_key = parent_eid if parent_eid else parent_tag
        count = self.increment_counter(parent_key, eid_value)
        new_eid = f"{eid_value}_o_{count}"
        return f"{parent_eid}__{new_eid}" if parent_eid else new_eid

    def set_element_attributes(self, element, tag, element_eid):
        """
        Sets the "eid" and "wid" attributes for the given element.
        assumes wid format is: <prefix>__<eid>

        Args:
            element: The element for which to set the attributes.
            tag: The tag of the element.
            element_eid: The element EWID.
        """
        if tag in ELEMENT_REF.__members__:
            element.set("eId", element_eid)
            element.set("wId", f"{self.wid_prefix}__{element_eid}")

    def fill_ewid(self, element, parent_eid="", parent_tag=""):
        """
        Fills the EWID for the given element and its children.

        Args:
            element: The element for which to fill the EWID.
            parent_eid: The parent EWID.
            parent_tag: The parent tag.
        """
        tag = element.tag
        element_eid = self.generate_eid(element, parent_eid, parent_tag)
        element_wid = f"{self.wid_prefix}__{element_eid}"
        self.set_element_attributes(element, tag, element_eid)

        # Remember the EWID for location annotated policy objects
        if "data-hint-object-code" in element.attrib or "data-hint-location" in element.attrib:
            object_code = element.get("data-hint-object-code", None)
            gebied_uuid = element.get("data-hint-gebied-uuid", None)
            # Store pairing in state
            self._state_manager.object_tekst_lookup[object_code] = {
                "wid": element_wid,
                "tag": element.tag,
                "gebied_uuid": gebied_uuid,
            }

        for child in element:
            child_parent_eid = element_eid if tag in ELEMENT_REF.__members__ else parent_eid
            self.fill_ewid(child, child_parent_eid, tag)

    def modify_xml(self, xml_source):
        """
        Modifies the XML by filling the EWID and returns the modified XML as a string.

        Args:
            xml_source: The XML source to modify.

        Returns:
            str: The modified XML as a string.
        """
        self.parse_xml(xml_source)
        if self.tree:
            self.fill_ewid(self.root)
            return ET.tostring(self.root, encoding="unicode")
        else:
            return None

    def write_to_file(self, output_file):
        """
        Writes the modified XML to the specified output file.

        Args:
            output_file: The output file to write to.
        """
        if self.tree:
            self.tree.write(output_file)
        else:
            print("No XML tree to write.")
