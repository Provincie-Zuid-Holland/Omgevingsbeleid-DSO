from typing import List

from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from dso.act_builder.state_manager.states.text_manipulator.extractor.werkingsgebieden_extractor import (
    TextWerkingsgebiedenExtractor,
)

from .......services.utils.helpers import load_template
from ......state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ......state_manager.state_manager import StateManager


class BijlageWerkingsgebiedenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._werkingsgebieden_extractor: TextWerkingsgebiedenExtractor = TextWerkingsgebiedenExtractor(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

    def create(self) -> str:
        all_werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        if len(all_werkingsgebieden) == 0:
            return ""

        werkingsgebieden = sorted(all_werkingsgebieden, key=lambda w: w.Title)

        content = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageWerkingsgebieden.xml",
            werkingsgebieden=werkingsgebieden,
        )

        content = self._state_manager.act_ewid_service.add_ewids(content)
        self._werkingsgebieden_extractor.extract(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content
