from typing import List

from dso.act_builder.state_manager.input_data.resource.document.document import Document

from .....services.utils.helpers import load_template
from ....state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from ....state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ....state_manager.state_manager import StateManager


class BesluitMetadataContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        informatieobject_refs: List[str] = []

        werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        for werkingsgebied in werkingsgebieden:
            if werkingsgebied.New:
                informatieobject_refs.append(werkingsgebied.Frbr.get_expression())

        documents: List[Document] = self._state_manager.input_data.resources.document_repository.all()
        for document in documents:
            if document.New:
                informatieobject_refs.append(document.Frbr.get_expression())

        pdfs: List[BesluitPdf] = self._state_manager.input_data.resources.besluit_pdf_repository.all()
        for pdf in pdfs:
            informatieobject_refs.append(pdf.frbr.get_expression())

        content = load_template(
            "akn/besluit_versie/BesluitMetadata.xml",
            besluit=self._state_manager.input_data.besluit,
            regeling_is_officieel=self._state_manager.input_data.regeling.is_officieel,
            provincie_ref=self._state_manager.input_data.publication_settings.provincie_ref,
            soort_bestuursorgaan=self._state_manager.input_data.publication_settings.soort_bestuursorgaan,
            informatieobject_refs=informatieobject_refs,
        )
        return content
