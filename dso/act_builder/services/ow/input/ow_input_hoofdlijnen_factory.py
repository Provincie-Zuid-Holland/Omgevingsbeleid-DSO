from typing import List

from dso.act_builder.services.ow.input.models import OwInputHoofdlijn
from dso.act_builder.state_manager.input_data.resource.hoofdlijn import Hoofdlijn, HoofdlijnRepository
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputHoofdlijnenFactory:
    def __init__(self, state_manager: StateManager):
        self._hoofdlijn_repository: HoofdlijnRepository = state_manager.input_data.resources.hoofdlijn_repository

    def get_hoofdlijnen(self):
        hoofdlijnen: List[Hoofdlijn] = self._hoofdlijn_repository.all()
        result: List[OwInputHoofdlijn] = []
        for hoofdlijn in hoofdlijnen:
            input_hoofdlijn: OwInputHoofdlijn = OwInputHoofdlijn(
                source_uuid=str(hoofdlijn.UUID),
                source_code=hoofdlijn.Code,
                title=hoofdlijn.Title,
                hoofdlijn_type=hoofdlijn.Hoofdlijn_Type,
            )
            result.append(input_hoofdlijn)
        return result
