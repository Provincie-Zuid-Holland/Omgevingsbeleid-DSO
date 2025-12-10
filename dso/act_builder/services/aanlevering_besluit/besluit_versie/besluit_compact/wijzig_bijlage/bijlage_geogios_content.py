from typing import List

from dso.act_builder.state_manager.states.text_manipulator.data_hint_cleaner import DataHintCleaner
from ......state_manager.input_data.resource.gebieden.types import GeoGio
from ......state_manager.state_manager import StateManager
from ......state_manager.states.text_manipulator.extractor.text_geogio_extractor import TextGeoGioExtractor
from .......services.utils.helpers import load_template


class BijlageGeoGioContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._geogio_extractor: TextGeoGioExtractor = TextGeoGioExtractor(state_manager)
        self._data_hint_cleaner: DataHintCleaner = DataHintCleaner()

    def create(self) -> str:
        all_geogios: List[GeoGio] = self._state_manager.input_data.resources.geogio_repository.all()
        if len(all_geogios) == 0:
            return ""

        sorted_geogios: List[GeoGio] = sorted(all_geogios, key=lambda g: g.title)

        content: str = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageGeoGios.xml",
            geogios=sorted_geogios,
        )

        content: str = self._state_manager.act_ewid_service.add_ewids(content)
        self._geogio_extractor.extract(content)
        content = self._data_hint_cleaner.cleanup_xml(content)

        return content
