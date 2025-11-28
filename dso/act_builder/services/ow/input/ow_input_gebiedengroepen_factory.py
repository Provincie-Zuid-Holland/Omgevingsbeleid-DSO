from typing import List

from dso.act_builder.services.ow.input.models import OwInputGebied, OwInputGebiedengroep
from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedengroep_repository import GebiedengroepRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied, GebiedenGroep
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputGebiedengroepenFactory:
    def __init__(self, state_manager: StateManager):
        self._groep_repository: GebiedengroepRepository = state_manager.input_data.resources.gebiedengroep_repository
        self._gebied_repository: GebiedRepository = state_manager.input_data.resources.gebied_repository

    def get_gebiedengroepen(self) -> List[OwInputGebiedengroep]:
        gebiedengroepen: List[GebiedenGroep] = self._groep_repository.all()
        result: List[OwInputGebiedengroep] = []

        for groep in gebiedengroepen:
            gebieden: List[Gebied] = self._gebied_repository.get_for_group(groep)
            input_gebieden: List[OwInputGebied] = [
                OwInputGebied(
                    source_uuid=str(gebied.uuid),
                    source_code=gebied.code,
                    geometry_id=gebied.identifier,
                    title=gebied.title,
                )
                for gebied in gebieden
            ]
            input_gebiedengroep = OwInputGebiedengroep(
                source_uuid=groep.uuid,
                source_code=groep.code,
                title=groep.title,
                gebieden=input_gebieden,
            )
            result.append(input_gebiedengroep)

        return result
