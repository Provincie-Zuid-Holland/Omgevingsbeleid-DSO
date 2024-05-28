from typing import List, Optional, Type
from uuid import UUID

from ....models import OwData, OwObjectMap, OwTekstdeelMap, OwIdMapping
from ....services.ow import (
    OWAmbtsgebied,
    OWDivisie,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWLocatie,
    OWObject,
    OWRegelingsgebied,
    OWTekstDeel,
)
from ..exceptions import OWStateMutationError


class OWStateRepository:
    def __init__(self, ow_input_data: OwData) -> None:
        # Previous ow state from input
        self._known_ow_state = ow_input_data
        self._merged_ow_state: Optional[OwData] = None

        self._new_ow_objects: List[OWObject] = []
        self._mutated_ow_objects: List[OWObject] = []
        self._terminated_ow_objects: List[OWObject] = []

    @property
    def changed_ow_objects(self) -> List[OWObject]:
        return self._new_ow_objects + self._mutated_ow_objects

    @property
    def changed_ow_object_ids(self) -> List[str]:
        return [ow.OW_ID for ow in self.changed_ow_objects]

    @property
    def terminated_ow_object_ids(self) -> List[str]:
        return [ow.OW_ID for ow in self._terminated_ow_objects]

    def add_new_ow(self, ow_object: OWObject) -> None:
        new_ow_id = ow_object.OW_ID
        if any(obj.OW_ID == new_ow_id for obj in self._new_ow_objects):
            raise OWStateMutationError(
                message="Cannot create ow object, already existing as new state object.",
                action="add_new_ow",
                ow_object=ow_object,
            )
        if any(obj.OW_ID == new_ow_id for obj in self._mutated_ow_objects):
            raise OWStateMutationError(
                message="Cannot create ow object, already added as mutated state object.",
                action="add_new_ow",
                ow_object=ow_object,
            )
        self._new_ow_objects.append(ow_object)

    def add_mutated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._known_ow_state.object_ids:
            raise OWStateMutationError(
                message="Cannot create ow object, already added as mutated state object.",
                action="add_mutated_ow",
                ow_object=ow_object,
            )
        # TODO: maybe add exception if mutating but no values changed? to prevent lvbb errors
        self._mutated_ow_objects.append(ow_object)

    def add_terminated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._known_ow_state.object_ids:
            raise OWStateMutationError(
                message="Cannot terminate ow object as it did not exist in input state.",
                action="add_terminated_ow",
                ow_object=ow_object,
            )
        self._terminated_ow_objects.append(ow_object)

    def get_new_locations(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, OWLocatie)]

    def get_mutated_locations(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, OWLocatie)]

    def get_terminated_locations(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, OWLocatie)]

    def get_new_div(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstDeel))]

    def get_mutated_div(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstDeel))]

    def get_terminated_div(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstDeel))]

    def get_new_regelingsgebied(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, OWRegelingsgebied)]

    def get_mutated_regelingsgebied(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, OWRegelingsgebied)]

    def get_terminated_regelingsgebied(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, OWRegelingsgebied)]

    def get_gebiedengroep_by_code(self, werkingsgebied_code: str) -> Optional[OWGebiedenGroep]:
        # Search current state used objects
        for ow_obj in self.changed_ow_objects:
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_active_ow_location_id(self, werkingsgebied_code: str) -> Optional[str]:
        # checks BOTH current state and input state for existing location id
        for obj in self.changed_ow_objects:
            if isinstance(obj, OWGebiedenGroep) and obj.mapped_geo_code == werkingsgebied_code:
                return obj.OW_ID

        return self.get_existing_gebiedengroep_id(werkingsgebied_code)

    def get_active_ambtsgebied(self) -> Optional[OWAmbtsgebied]:
        for ow_obj in self.changed_ow_objects:
            if isinstance(ow_obj, OWAmbtsgebied):
                return ow_obj
        return None

    # KNOWN STATE MAP LOOKUPS
    # TODO: change to full OW object structure instead
    def get_existing_gebied_id(self, werkingsgebied_code: str) -> Optional[str]:
        gebied_map = self._known_ow_state.object_map.id_mapping.gebieden
        return gebied_map.get(werkingsgebied_code, None)

    def get_existing_gebiedengroep_id(self, werkingsgebied_code: str) -> Optional[str]:
        gebiedengroep_map = self._known_ow_state.object_map.id_mapping.gebiedengroep
        return gebiedengroep_map.get(werkingsgebied_code, None)

    def get_existing_ambtsgebied_id(self, uuid: UUID) -> Optional[str]:
        ambtsgebied_map = self._known_ow_state.object_map.id_mapping.ambtsgebied
        return ambtsgebied_map.get(str(uuid), None)

    def get_existing_regelingsgebied_id(self, ambtsgebied_ow_id: str) -> Optional[str]:
        regelingsgebied_map = self._known_ow_state.object_map.id_mapping.regelingsgebied
        return regelingsgebied_map.get(ambtsgebied_ow_id, None)

    def get_existing_divisie(self, wid: str) -> Optional[OWDivisieTekst]:
        wid_map = self._known_ow_state.object_map.id_mapping.wid
        ow_divisie_id = wid_map.get(wid, None)
        return OWDivisieTekst(OW_ID=ow_divisie_id, wid=wid) if ow_divisie_id else None

    def get_existing_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstDeel]:
        existing_tekstdeel_map = self._known_ow_state.object_map.tekstdeel_mapping
        for tekstdeel_ow_id, values in existing_tekstdeel_map.items():
            if values.divisie == divisie_ow_id:
                return OWTekstDeel(OW_ID=tekstdeel_ow_id, locaties=[values.location], divisie=divisie_ow_id)
        return None

    def get_existing_wid_list(self) -> List[str]:
        existing_id_map = self._known_ow_state.object_map.id_mapping
        wid_map = existing_id_map.wid
        return list(wid_map.keys())

    def get_existing_werkingsgebied_code_by_divisie(self, divisie_ow_id: str) -> Optional[str]:
        # ow_data state map could be changed to make these lookups less complex
        # for now we fetch the werkingsgebied-code <-> divisie_ow_id combination from the
        # previous state by backtracking the matching tekstdeel objects
        existing_id_map = self._known_ow_state.object_map.id_mapping
        ow_tekstdeel = self.get_existing_tekstdeel_by_divisie(divisie_ow_id)

        if not existing_id_map or not ow_tekstdeel:
            return None

        for werkingsgebied_code, gebiedengroep_id in existing_id_map.gebiedengroep.items():
            if gebiedengroep_id in ow_tekstdeel.locaties:
                return werkingsgebied_code

        return None

    def _merge_ow_object_ids(
        self, input_obj_ids: List[str], changed_obj_ids: List[str], terminated_obj_ids: List[str]
    ) -> List[str]:
        updated_object_list = set(input_obj_ids)
        updated_object_list.update(changed_obj_ids)
        updated_object_list.difference_update(terminated_obj_ids)
        return list(updated_object_list)

    def _merge_ow_object_map(
        self, input_obj_map: OwObjectMap, changed_objs: List[OWObject], terminated_objs: List[OWObject]
    ) -> OwObjectMap:
        # For each new or mutated OWObject, add or updateit to the object_map
        for ow_obj in changed_objs:
            if isinstance(ow_obj, OWGebied):
                input_obj_map.id_mapping.gebieden[ow_obj.mapped_geo_code] = ow_obj.OW_ID
            if isinstance(ow_obj, OWGebiedenGroep):
                input_obj_map.id_mapping.gebiedengroep[ow_obj.mapped_geo_code] = ow_obj.OW_ID
            if isinstance(ow_obj, OWAmbtsgebied):
                input_obj_map.id_mapping.ambtsgebied[ow_obj.mapped_uuid] = ow_obj.OW_ID
            if isinstance(ow_obj, OWRegelingsgebied):
                input_obj_map.id_mapping.regelingsgebied[ow_obj.ambtsgebied] = ow_obj.OW_ID
            if isinstance(ow_obj, OWDivisie) or isinstance(ow_obj, OWDivisieTekst):
                input_obj_map.id_mapping.wid[ow_obj.wid] = ow_obj.OW_ID
            if isinstance(ow_obj, OWTekstDeel):
                input_obj_map.tekstdeel_mapping[ow_obj.OW_ID] = {
                    "divisie": ow_obj.divisie,
                    "location": ow_obj.locaties[0],
                }

        # For each terminated OWObject, remove the corresponding entry from the object_map
        for ow_obj in terminated_objs:
            if isinstance(ow_obj, OWGebied):
                del input_obj_map.id_mapping.gebieden[ow_obj.mapped_geo_code]
            if isinstance(ow_obj, OWGebiedenGroep):
                del input_obj_map.id_mapping.gebiedengroep[ow_obj.mapped_geo_code]
            if isinstance(ow_obj, OWAmbtsgebied):
                del input_obj_map.id_mapping.ambtsgebied[ow_obj.mapped_uuid]
            if isinstance(ow_obj, OWRegelingsgebied):
                del input_obj_map.id_mapping.regelingsgebied[ow_obj.ambtsgebied]
            if isinstance(ow_obj, OWDivisie) or isinstance(ow_obj, OWDivisieTekst):
                del input_obj_map.id_mapping.wid[ow_obj.wid]
            if isinstance(ow_obj, OWTekstDeel):
                del input_obj_map.tekstdeel_mapping[ow_obj.OW_ID]

        return input_obj_map

    def merge_ow_state(self) -> None:
        """
        Merge the previous OW state with our changes to create a new patched ow object state.
        New objects are added, mutated objects are updated, and terminated objects are removed.
        """

        new_ow_state = self._known_ow_state.copy(deep=True)

        # Update the object_ids list with new entries
        new_obj_ids = self._merge_ow_object_ids(
            input_obj_ids=new_ow_state.object_ids,
            changed_obj_ids=self.changed_ow_object_ids,
            terminated_obj_ids=self.terminated_ow_object_ids,
        )

        # Update the object map
        new_obj_map = self._merge_ow_object_map(
            input_obj_map=new_ow_state.object_map,
            changed_objs=self.changed_ow_objects,
            terminated_objs=self._terminated_ow_objects,
        )

        new_ow_state.object_ids = new_obj_ids
        new_ow_state.object_map = new_obj_map

        self._merged_ow_state = new_ow_state

    def get_merged_ow_state(self) -> OwData:
        if self._merged_ow_state is None:
            self.merge_ow_state()

        return self._merged_ow_state
