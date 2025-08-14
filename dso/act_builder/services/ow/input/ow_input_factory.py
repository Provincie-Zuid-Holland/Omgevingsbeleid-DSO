from typing import List

from dso.act_builder.services.ow.input.models import (
    OwInputAmbtsgebied,
    OwInputGebiedsaanwijzing,
    OwInputPolicyObject,
    OwInputRegelingsgebied,
    OwInputWerkingsgebied,
)
from dso.act_builder.services.ow.input.ow_input_ambtsgebied_factory import OwInputAmbtsgebiedFactory
from dso.act_builder.services.ow.input.ow_input_gebiedsaanwijzing_factory import OwInputGebiedsaanwijzingFactory
from dso.act_builder.services.ow.input.ow_input_policy_object_factory import OwInputPolicyObjectFactory
from dso.act_builder.services.ow.input.ow_input_regelingsgebied_factory import OwInputRegelingsgebiedFactory
from dso.act_builder.services.ow.input.ow_input_werkingsgebieden_factory import OwInputWerkingsgebiedenFactory
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputFactory:
    def __init__(self, state_manager: StateManager):
        self._ambtsgebied_factory: OwInputAmbtsgebiedFactory = OwInputAmbtsgebiedFactory(state_manager)
        self._regelingsgebied_factory: OwInputRegelingsgebiedFactory = OwInputRegelingsgebiedFactory(state_manager)
        self._werkingsgebieden_factory: OwInputWerkingsgebiedenFactory = OwInputWerkingsgebiedenFactory(state_manager)
        self._gebiedsaanwijzingen_factory: OwInputGebiedsaanwijzingFactory = OwInputGebiedsaanwijzingFactory(
            state_manager
        )
        self._policy_object_factory: OwInputPolicyObjectFactory = OwInputPolicyObjectFactory(state_manager)

    def get_ambtsgebied(self) -> OwInputAmbtsgebied:
        return self._ambtsgebied_factory.get_ambtsgebied()

    def get_regelingsgebied(self) -> OwInputRegelingsgebied:
        return self._regelingsgebied_factory.get_regelingsgebied()

    def get_gebiedsaanwijzingen(self) -> List[OwInputGebiedsaanwijzing]:
        return self._gebiedsaanwijzingen_factory.get_gebiedsaanwijzingen()

    def get_policy_objects(self) -> List[OwInputPolicyObject]:
        return self._policy_object_factory.get_policy_objects()

    def get_werkingsgebieden(self) -> List[OwInputWerkingsgebied]:
        return self._werkingsgebieden_factory.get_werkingsgebieden()
