from typing import Dict, List, Set, Optional


from ...act_builder.state_manager.states.ow_repository import OWStateRepository
from ...act_builder.state_manager.exceptions import OWStateDanglingObjectsException
from ...models import OwData
from .models import OWObject, OWGebiedenGroep, OWTekstdeel, OWRegelingsgebied, OWGebied


class OWStatePatcher:
    def __init__(self, ow_data: OwData, ow_repository: OWStateRepository):
        self._known_ow_state = ow_data
        self._ow_repository: OWStateRepository = ow_repository
        self._patched_ow_state: Optional[OwData] = None  # result state

    def get_patched_ow_state(self) -> OwData:
        if self._patched_ow_state is None:
            raise ValueError("OW state not patched yet.")
        return self._patched_ow_state

    def patch(self) -> None:
        """merge changed and terminated ow objects into the known ow state"""
        new_ow_state: OwData = self._known_ow_state.copy(deep=True)

        # update active ow_objects
        for ow_obj in self._ow_repository.get_changed_ow_objects():
            new_ow_state.ow_objects[ow_obj.OW_ID] = ow_obj

        for ow_obj in self._ow_repository.get_terminated_ow_objects():
            del new_ow_state.ow_objects[ow_obj.OW_ID]
            new_ow_state.terminated_ow_ids.append(ow_obj.OW_ID)

        # ensure isolated objects are terminated
        new_ow_state = self._remove_dangling_objects(new_ow_state)
        self._patched_ow_state = new_ow_state

    def _remove_dangling_objects(self, new_ow_state):
        """
        Check for objects that are not referenced by any other objects and remove them.
        Its possible a termination creates a new dangling objects, so we repeat until result is 0.
        """
        while True:
            # Build relationship index
            reverse_ref_index = self._build_reverse_ref_index(new_ow_state.ow_objects)
            # Check for objects without references
            dangling_objects = self._find_dangling_objects(
                ow_objects=new_ow_state.ow_objects.values(),
                used_ow_ids=new_ow_state.used_ow_ids,
                ref_index=reverse_ref_index,
            )

            if not dangling_objects:  # finished if no more dangling objects
                break

            for dangling_obj in dangling_objects:
                del new_ow_state.ow_objects[dangling_obj.OW_ID]
                new_ow_state.terminated_ow_ids.append(dangling_obj.OW_ID)
                dangling_obj.set_status_beeindig()
                self._ow_repository.add_terminated_ow(dangling_obj)

                # since we currently still keep every owgebied to one owgebiedengroep,
                # we can cascade delete its owgebied ref objects
                if isinstance(dangling_obj, OWGebiedenGroep):
                    for gebied_ref in dangling_obj.gebieden:
                        gebied_obj = new_ow_state.ow_objects.get(gebied_ref)
                        if isinstance(gebied_obj, OWGebied):
                            del new_ow_state.ow_objects[gebied_obj.OW_ID]
                            new_ow_state.terminated_ow_ids.append(gebied_obj.OW_ID)
                            gebied_obj.set_status_beeindig()
                            self._ow_repository.add_terminated_ow(gebied_obj)

        return new_ow_state

    def _build_reverse_ref_index(self, ow_objects_map: Dict[str, "OWObject"]) -> Dict[str, Set[str]]:
        reverse_ref_index = {
            "OWTekstdeel": set(),
            "OWGebiedenGroep": set(),
            "OWRegelingsgebied": set(),
        }

        for ow_obj in ow_objects_map.values():
            if isinstance(ow_obj, OWTekstdeel):
                for locatie_id in ow_obj.locaties:
                    reverse_ref_index["OWTekstdeel"].add(locatie_id)
                reverse_ref_index["OWTekstdeel"].add(ow_obj.divisie)
            if isinstance(ow_obj, OWGebiedenGroep):
                for gebied_id in ow_obj.gebieden:
                    reverse_ref_index["OWGebiedenGroep"].add(gebied_id)
            if isinstance(ow_obj, OWRegelingsgebied):
                reverse_ref_index["OWRegelingsgebied"].add(ow_obj.ambtsgebied)

        return reverse_ref_index

    def _find_dangling_objects(
        self, ow_objects: List[OWObject], used_ow_ids: List[str], ref_index: dict
    ) -> List["OWObject"]:
        """Check for OWObjects that are not referenced by any other objects."""
        dangling_objects: List["OWObject"] = []

        # Collect IDs from all relationships
        for ow_obj in ow_objects:
            if not ow_obj.has_valid_refs(used_ow_ids, ref_index):
                dangling_objects.append(ow_obj)

        return dangling_objects
