from typing import List

from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from ......state_manager.input_data.resource.gebieden.types import Gio
from ......state_manager.state_manager import StateManager
from ......state_manager.states.text_manipulator.extractor.text_gio_extractor import TextGioExtractor
from .......services.utils.helpers import load_template


class BijlageGioContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._gio_extractor: TextGioExtractor = TextGioExtractor(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

    def create(self) -> str:
        all_gios: List[Gio] = self._state_manager.input_data.resources.gio_repository.all()
        if len(all_gios) == 0:
            return ""

        sorted_gios: List[Gio] = sorted(all_gios, key=lambda g: g.title)

        content: str = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageGios.xml",
            gios=sorted_gios,
        )

        content: str = self._state_manager.act_ewid_service.add_ewids(content)
        self._gio_extractor.extract(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content
