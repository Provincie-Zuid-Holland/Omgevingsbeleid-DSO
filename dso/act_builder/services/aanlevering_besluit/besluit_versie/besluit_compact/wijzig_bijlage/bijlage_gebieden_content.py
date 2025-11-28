from typing import List

from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from ......state_manager.input_data.resource.gebieden.types import Gebied
from ......state_manager.state_manager import StateManager
from ......state_manager.states.text_manipulator.extractor.gebieden_extractor import TextGebiedenExtractor
from .......services.utils.helpers import load_template


class BijlageGebiedenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._gebieden_extractor: TextGebiedenExtractor = TextGebiedenExtractor(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

    def create(self) -> str:
        all_gebieden: List[Gebied] = self._state_manager.input_data.resources.gebied_repository.all()
        if len(all_gebieden) == 0:
            return ""

        gebieden: List[Gebied] = sorted(all_gebieden, key=lambda g: g.title)

        content: str = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageGebieden.xml",
            gebieden=gebieden,
        )

        content: str = self._state_manager.act_ewid_service.add_ewids(content)
        self._gebieden_extractor.extract(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content
