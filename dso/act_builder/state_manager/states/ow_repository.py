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
        self._patched_ow_state: Optional[OwData] = None

        self._new_ow_objects: List[OWObject] = []
        self._mutated_ow_objects: List[OWObject] = []
        self._terminated_ow_objects: List[OWObject] = []

    @property
    def pending_ow_objects(self) -> List[OWObject]:
        """
        OW objects changed from the previous state, that are pending
        to be used in the output files (excluding terminated objects)
        """
        return self._new_ow_objects + self._mutated_ow_objects

    @property
    def pending_ow_object_ids(self) -> List[str]:
        ow_id_list = [ow.OW_ID for ow in self.pending_ow_objects]
        return ow_id_list

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
        for ow_obj in self.pending_ow_objects:
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_active_ow_location_id(self, werkingsgebied_code: str) -> Optional[str]:
        # checks BOTH current state and input state for existing location id
        for obj in self.pending_ow_objects:
            if isinstance(obj, OWGebiedenGroep) and obj.mapped_geo_code == werkingsgebied_code:
                return obj.OW_ID

        return self.get_existing_gebiedengroep_id(werkingsgebied_code)

    def get_active_ambtsgebied(self) -> Optional[OWAmbtsgebied]:
        for ow_obj in self.pending_ow_objects:
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

    def patch_gebieden_mapping(self, ow_object_state: OwData, locatie_ow_id: str, werkingsgebied_code: str) -> None:
        ow_object_state.object_map.id_mapping.gebieden[werkingsgebied_code] = locatie_ow_id

    def remove_gebieden_mapping(self, werkingsgebied_code: str) -> None:
        del self._known_ow_state.object_map.id_mapping.gebieden[werkingsgebied_code]

    def _merge_ow_object_map(self, ow_object_map: OwObjectMap):
        # For each new or mutated OWObject, add or updateit to the object_map
        for ow_obj in self.pending_ow_objects:
            if isinstance(ow_obj, OWGebied):
                ow_object_map.id_mapping.gebieden[ow_obj.mapped_geo_code] = ow_obj.OW_ID
            if isinstance(ow_obj, OWGebiedenGroep):
                ow_object_map.id_mapping.gebiedengroep[ow_obj.mapped_geo_code] = ow_obj.OW_ID
            if isinstance(ow_obj, OWAmbtsgebied):
                ow_object_map.id_mapping.ambtsgebied[ow_obj.mapped_uuid] = ow_obj.OW_ID
            if isinstance(ow_obj, OWRegelingsgebied):
                ow_object_map.id_mapping.regelingsgebied[ow_obj.ambtsgebied] = ow_obj.OW_ID
            if isinstance(ow_obj, OWDivisie) or isinstance(ow_obj, OWDivisieTekst):
                ow_object_map.id_mapping.wid[ow_obj.wid] = ow_obj.OW_ID
            if isinstance(ow_obj, OWTekstDeel):
                ow_object_map.tekstdeel_mapping[ow_obj.OW_ID] = {
                    "divisie": ow_obj.divisie,
                    "location": ow_obj.locaties[0],
                }

        # For each terminated OWObject, remove the corresponding entry from the object_map
        for ow_obj in self._terminated_ow_objects:
            if isinstance(ow_obj, OWGebied):
                del ow_object_map.id_mapping.gebieden[ow_obj.mapped_geo_code]
            if isinstance(ow_obj, OWGebiedenGroep):
                del ow_object_map.id_mapping.gebiedengroep[ow_obj.mapped_geo_code]
            if isinstance(ow_obj, OWAmbtsgebied):
                del ow_object_map.id_mapping.ambtsgebied[ow_obj.mapped_uuid]
            if isinstance(ow_obj, OWRegelingsgebied):
                del ow_object_map.id_mapping.regelingsgebied[ow_obj.ambtsgebied]
            if isinstance(ow_obj, OWDivisie) or isinstance(ow_obj, OWDivisieTekst):
                del ow_object_map.id_mapping.wid[ow_obj.wid]
            if isinstance(ow_obj, OWTekstDeel):
                del ow_object_map.tekstdeel_mapping[ow_obj.OW_ID]

        return ow_object_map

    def create_patched_ow_state(self) -> OwData:
        """
        Merge the previous OW state with our changes to create a new patched ow object state.
        New objects are added, mutated objects are updated, and terminated objects are removed.
        """
        if self._patched_ow_state is not None:
            return self._patched_ow_state

        patched_ow_state = self._known_ow_state.copy(deep=True)

        # Update the object_ids list with new entries
        patched_ow_state.object_ids = list(set(self._known_ow_state.object_ids + self.pending_ow_object_ids))
        # TODO: remove terminated from list

        # Update the object map
        patched_object_map = self._merge_ow_object_map(patched_ow_state.object_map)
        patched_ow_state.object_map = patched_object_map

        self._patched_ow_state = patched_ow_state
        return patched_ow_state
