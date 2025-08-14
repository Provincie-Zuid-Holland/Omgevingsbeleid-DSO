from typing import List, Optional

from dso.act_builder.services.ow.input.models import (
    OwInputAbstractLocatieRef,
    OwInputAmbtsgebiedLocatieRef,
    OwInputPolicyObject,
    OwInputWerkingsgebiedLocatieRef,
)
from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object import PolicyObject
from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object_repository import (
    PolicyObjectRepository,
)
from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.models import TekstPolicyObject, TextData


class OwInputPolicyObjectFactory:
    def __init__(self, state_manager: StateManager):
        self._werkingsgebieden_repository: WerkingsgebiedRepository = (
            state_manager.input_data.resources.werkingsgebied_repository
        )
        self._policy_object_repository: PolicyObjectRepository = (
            state_manager.input_data.resources.policy_object_repository
        )
        self._text_data: TextData = state_manager.text_data

    def get_policy_objects(self) -> List[OwInputPolicyObject]:
        result: List[OwInputPolicyObject] = []

        for tekst_policy_object in self._text_data.policy_objects:
            ow_input_policy_object: OwInputPolicyObject = self._build_ow_input_policy_object(tekst_policy_object)
            result.append(ow_input_policy_object)

        return result

    def _build_ow_input_policy_object(self, tekst_policy_object: TekstPolicyObject) -> OwInputPolicyObject:
        policy_object: PolicyObject = self._policy_object_repository.get_by_code(tekst_policy_object.object_code)
        policy_object_data: dict = policy_object.get_data()

        location_refs: List[OwInputAbstractLocatieRef] = self._get_location_refs(policy_object)

        result = OwInputPolicyObject(
            source_uuid=str(policy_object_data["UUID"]),
            source_code=tekst_policy_object.object_code,
            wid=tekst_policy_object.wid,
            element=tekst_policy_object.element.lower(),
            location_refs=location_refs,
        )
        return result

    def _get_location_refs(self, policy_object: PolicyObject) -> List[OwInputAbstractLocatieRef]:
        if not policy_object.has_werkingsgebied():
            return []

        werkingsgebied_code: Optional[str] = policy_object.get_werkingsgebied()
        if werkingsgebied_code is None:
            return [OwInputAmbtsgebiedLocatieRef()]

        return [OwInputWerkingsgebiedLocatieRef(code=werkingsgebied_code)]
