from typing import List

from lxml import etree

from dso.act_builder.state_manager.input_data.resource.document.document import Document

from .......services.utils.helpers import load_template
from ......state_manager.state_manager import StateManager


class BijlageDocumentenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        documenten: List[Document] = self._state_manager.input_data.resources.document_repository.all()
        documenten = sorted(documenten, key=lambda d: d.Title)
        if len(documenten) == 0:
            return ""

        content = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageDocumenten.xml",
            documenten=documenten,
        )

        content = self._state_manager.act_ewid_service.add_ewids(content)
        content = self._create_documenten_wid_lookup(content)
        content = self._remove_hints(content)

        return content

    def _create_documenten_wid_lookup(self, xml_content: str):
        root = etree.fromstring(xml_content)
        elements = root.xpath("//*[@data-hint-document-uuid]")

        for element in elements:
            uuid = element.get("data-hint-document-uuid")
            self._state_manager.document_eid_lookup[uuid] = element.get("eId")
            self._state_manager.document_wid_lookup[uuid] = element.get("wId")

        return etree.tostring(root, encoding="unicode", pretty_print=True)

    def _remove_hints(self, xml_data: str) -> str:
        xml_data = self._clean_attribute(xml_data, "data-hint-wid-code")
        xml_data = self._clean_attribute(xml_data, "data-hint-document-uuid")
        return xml_data

    def _clean_attribute(self, xml_data: str, attribute: str) -> str:
        root = etree.fromstring(xml_data)
        for element in root.xpath(f"//*[@{attribute}]"):
            element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
