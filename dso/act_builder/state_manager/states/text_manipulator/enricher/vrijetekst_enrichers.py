from typing import List

from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher
from dso.act_builder.state_manager.states.text_manipulator.enricher.document_intref_enricher import (
    DocumentIntrefEnricher,
)
from dso.act_builder.state_manager.states.text_manipulator.enricher.gebiedsaanwijzing_intref_enricher import GebiedsaanwijzingIntrefEnricher
from dso.act_builder.state_manager.states.text_manipulator.enricher.illustration_enricher import IllustrationEnricher
from dso.act_builder.state_manager.states.text_manipulator.enricher.object_intref_enricher import ObjectIntrefEnricher


class VrijetekstEnrichers:
    def __init__(self, state_manager: StateManager):
        self._enrichers: List[AbstractEnricher] = [
            IllustrationEnricher(state_manager),
            DocumentIntrefEnricher(state_manager),
            ObjectIntrefEnricher(state_manager),
            GebiedsaanwijzingIntrefEnricher(state_manager),
        ]

    def enrich_xml(self, xml_content: str) -> str:
        for enricher in self._enrichers:
            xml_content = enricher.enrich_xml(xml_content)

        return xml_content
