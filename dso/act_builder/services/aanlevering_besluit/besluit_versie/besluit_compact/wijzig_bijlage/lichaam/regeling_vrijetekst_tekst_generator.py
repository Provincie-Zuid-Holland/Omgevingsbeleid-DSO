from bs4 import BeautifulSoup

from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from dso.act_builder.state_manager.states.text_manipulator.enricher.vrijetekst_enrichers import VrijetekstEnrichers
from dso.act_builder.state_manager.states.text_manipulator.extractor.policy_object_extractor import (
    TextPolicyObjectExtractor,
)

from ........services.tekst.middleware import middleware_enrich_table
from ........services.tekst.tekst import Lichaam
from ........services.utils.helpers import is_html_valid
from .......state_manager.state_manager import StateManager


class RegelingVrijetekstTekstGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._policy_object_extractor: TextPolicyObjectExtractor = TextPolicyObjectExtractor(state_manager)
        self._vrijetekst_enrichers: VrijetekstEnrichers = VrijetekstEnrichers(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

    def create(self, html: str):
        content: str = self._html_to_xml_lichaam(html)
        content = self._state_manager.act_ewid_service.add_ewids(content)

        self._policy_object_extractor.extract(content)

        content = self._vrijetekst_enrichers.enrich_xml(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content

    def _html_to_xml_lichaam(self, html: str) -> str:
        if not is_html_valid(html):
            raise RuntimeError("Invalid html")

        html = middleware_enrich_table(html)
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Lichaam()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml
