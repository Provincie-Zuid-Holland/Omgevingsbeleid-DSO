from dso.act_builder.services.ow.input.models import OwInputRegelingsgebied
from dso.act_builder.state_manager.input_data.ambtsgebied import Ambtsgebied
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputRegelingsgebiedFactory:
    def __init__(self, state_manager: StateManager):
        self._ambtsgebied: Ambtsgebied = state_manager.input_data.ambtsgebied

    def get_regelingsgebied(self) -> OwInputRegelingsgebied:
        result = OwInputRegelingsgebied(
            source_uuid=str(self._ambtsgebied.UUID),
        )

        return result
