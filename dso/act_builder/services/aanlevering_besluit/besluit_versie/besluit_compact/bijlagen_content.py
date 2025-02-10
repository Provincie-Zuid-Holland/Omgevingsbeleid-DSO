from typing import List

from dso.act_builder.services.services.appendices_service import AppendicesService, AppendixDestination

from .....state_manager.input_data.besluit import Bijlage
from .....state_manager.state_manager import StateManager


class BijlagenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._appendices_service: AppendicesService = AppendicesService(state_manager)

    def create(self) -> str:
        appendices: List[Bijlage] = self._state_manager.input_data.besluit.bijlagen
        result: str = self._appendices_service.generate_xml(
            AppendixDestination.BILL,
            appendices,
        )

        return result
