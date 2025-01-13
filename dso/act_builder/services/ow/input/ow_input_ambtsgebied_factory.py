from dso.act_builder.services.ow.input.models import OwInputAmbtsgebied
from dso.act_builder.state_manager.input_data.ambtsgebied import Ambtsgebied
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputAmbtsgebiedFactory:
    def __init__(self, state_manager: StateManager):
        self._ambtsgebied: Ambtsgebied = state_manager.input_data.ambtsgebied

    def get_ambtsgebied(self) -> OwInputAmbtsgebied:
        result = OwInputAmbtsgebied(
            source_uuid=str(self._ambtsgebied.UUID),
            administrative_borders_id=self._ambtsgebied.identificatie_suffix,
            domain=self._ambtsgebied.domein,
            valid_on=self._ambtsgebied.geldig_op,
            title=self._ambtsgebied.titel,
        )

        return result
