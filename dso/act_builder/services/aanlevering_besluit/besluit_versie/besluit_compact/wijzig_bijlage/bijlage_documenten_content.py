from typing import List

from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from dso.act_builder.state_manager.states.text_manipulator.extractor.documenten_extractor import TextDocumentenExtractor

from .......services.utils.helpers import load_template
from ......state_manager.state_manager import StateManager


class BijlageDocumentenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._document_extractor: TextDocumentenExtractor = TextDocumentenExtractor(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

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
        self._document_extractor.extract(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content
