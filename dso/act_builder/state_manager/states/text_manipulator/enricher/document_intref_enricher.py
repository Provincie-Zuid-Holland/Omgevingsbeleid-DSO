from lxml import etree

from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher
from dso.act_builder.state_manager.states.text_manipulator.models import TekstBijlageDocument, TextData


class DocumentIntrefEnricher(AbstractEnricher):
    def __init__(self, state_manager: StateManager):
        self._text_data: TextData = state_manager.text_data

    def enrich_xml(self, xml_content: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        for intref in root.xpath("//IntIoRef[@data-hint-document-code]"):
            document_code: str = intref.get("data-hint-document-code")
            text_document: TekstBijlageDocument = self._text_data.get_document_by_code(document_code)

            intref.set("ref", text_document.wid)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
