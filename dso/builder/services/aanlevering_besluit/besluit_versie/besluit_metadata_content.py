from typing import List

from .....services.utils.helpers import load_template
from ....state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ....state_manager.state_manager import StateManager


class BesluitMetadataContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        informatieobject_refs: List[str] = []
        for werkingsgebied in werkingsgebieden:
            if werkingsgebied.New:
                informatieobject_refs.append(werkingsgebied.get_FRBR().expression)

        content = load_template(
            "akn/besluit_versie/BesluitMetadata.xml",
            besluit=self._state_manager.input_data.besluit,
            provincie_ref=self._state_manager.input_data.publication_settings.provincie_ref,
            soort_bestuursorgaan=self._state_manager.input_data.publication_settings.soort_bestuursorgaan,
            informatieobject_refs=informatieobject_refs,
        )
        return content
