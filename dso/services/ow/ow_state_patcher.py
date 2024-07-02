from typing import List, Optional

from ...models import OwData
from .models import OWObject


class OWStatePatcher:
    def __init__(self, ow_data: OwData, changed_ow_objects: List[OWObject], terminated_ow_objects: List[OWObject]):
        self._known_ow_state = ow_data
        self._changed_ow_objects = changed_ow_objects
        self._terminated_ow_objects = terminated_ow_objects
        self._patched_ow_state: Optional[OwData] = None  # result state

    @property
    def patched_ow_state(self) -> OwData:
        if self._patched_ow_state is None:
            raise ValueError("OW state not patched yet.")
        return self._patched_ow_state

    def _patch_used_ow_ids(
        self, input_obj_ids: List[str], changed_obj_ids: List[str], terminated_obj_ids: List[str]
    ) -> List[str]:
        """take existing ow ids and update with new, changed, terminated ids"""
        updated_object_list = set(input_obj_ids)
        updated_object_list.update(changed_obj_ids)
        updated_object_list.difference_update(terminated_obj_ids)
        return list(updated_object_list)

    def patch(self) -> None:
        """merge changed and terminated ow objects into the known ow state"""
        changed_obj_ids = [obj.OW_ID for obj in self._changed_ow_objects]
        terminated_obj_ids = [obj.OW_ID for obj in self._terminated_ow_objects]

        new_ow_state: OwData = self._known_ow_state.copy(deep=True)

        new_ow_state.used_ow_ids = self._patch_used_ow_ids(
            new_ow_state.used_ow_ids,
            changed_obj_ids=changed_obj_ids,
            terminated_obj_ids=terminated_obj_ids,
        )

        # update active ow_objects
        for ow_obj in self._changed_ow_objects:
            new_ow_state.ow_objects[ow_obj.OW_ID] = ow_obj

        for ow_obj in self._terminated_ow_objects:
            del new_ow_state.ow_objects[ow_obj.OW_ID]
            new_ow_state.terminated_ow_ids.append(ow_obj.OW_ID)

        self._patched_ow_state = new_ow_state
