from typing import Dict, List, Optional

from dso import Thema, ThemaFactory
from dso.act_builder.services.ow.input.models import OwInputThema
from dso.act_builder.state_manager import StateManager
from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object_repository import (
    PolicyObjectRepository,
)


class OwInputThemaFactory:
    def __init__(self, state_manager: StateManager):
        self._policy_object_repository: PolicyObjectRepository = (
            state_manager.input_data.resources.policy_object_repository
        )
        self._thema_types: Dict[str, Thema] = ThemaFactory().get_all()

    def get_themas(self) -> List[OwInputThema]:
        themas: List[str] = [
            thema for policy_object in self._policy_object_repository.get_all() for thema in policy_object.get_themas()
        ]
        result: List[OwInputThema] = []
        for thema in themas:
            maybe_thema: Optional[Thema] = self._thema_types.get(thema)
            if maybe_thema is None:
                raise RuntimeError(f"Thema unknown '{maybe_thema}'")
            result.append(OwInputThema(label=maybe_thema.label, uri=maybe_thema.uri))
        return result
