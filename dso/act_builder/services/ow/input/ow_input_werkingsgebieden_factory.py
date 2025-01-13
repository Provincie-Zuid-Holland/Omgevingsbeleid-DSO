from typing import List

from dso.act_builder.services.ow.input.models import OwInputLocatie, OwInputWerkingsgebied
from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputWerkingsgebiedenFactory:
    def __init__(self, state_manager: StateManager):
        self._werkingsgebieden_repository: WerkingsgebiedRepository = (
            state_manager.input_data.resources.werkingsgebied_repository
        )

    def get_werkingsgebieden(self) -> List[OwInputWerkingsgebied]:
        result: List[OwInputWerkingsgebied] = []

        for werkingsgebied in self._werkingsgebieden_repository.all():
            input_locations = [
                OwInputLocatie(
                    source_uuid=str(l.UUID),
                    source_code=f"{werkingsgebied.Code}-{i}",
                    geometry_id=l.Identifier,
                    title=l.Title,
                )
                for i, l in enumerate(werkingsgebied.Locaties)
            ]
            input_werkingsgebied = OwInputWerkingsgebied(
                source_uuid=werkingsgebied.Identifier,
                source_code=werkingsgebied.Code,
                title=werkingsgebied.Title,
                locations=input_locations,
            )
            result.append(input_werkingsgebied)

        return result
