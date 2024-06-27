from typing import List, Optional
from uuid import UUID

from ....models import OwData
from ....services.ow import (
    OWAmbtsgebied,
    OWDivisie,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWLocatie,
    OWObject,
    OWRegelingsgebied,
    OWTekstdeel,
)
from ..exceptions import OWStateMutationError


class OWStateRepository:
    def __init__(self, ow_input_data: OwData) -> None:
        # Previous ow state from input
        self._known_ow_state = ow_input_data

        self._new_ow_objects: List[OWObject] = []
        self._mutated_ow_objects: List[OWObject] = []
        self._terminated_ow_objects: List[OWObject] = []

    @property
    def changed_ow_objects(self) -> List[OWObject]:
        return self._new_ow_objects + self._mutated_ow_objects

    @property
    def terminated_ow_objects(self) -> List[OWObject]:
        return self._terminated_ow_objects

    def add_new_ow(self, ow_object: OWObject) -> None:
        new_ow_id = ow_object.OW_ID
        if any(obj.OW_ID == new_ow_id for obj in self._new_ow_objects):
            raise OWStateMutationError(
                message="Cannot create ow object, already existing as new state object.",
                action="add_new_ow",
                ow_object=ow_object.dict(),
            )
        if any(obj.OW_ID == new_ow_id for obj in self._mutated_ow_objects):
            raise OWStateMutationError(
                message="Cannot create ow object, already added as mutated state object.",
                action="add_new_ow",
                ow_object=ow_object.dict(),
            )
        self._new_ow_objects.append(ow_object)

    def add_mutated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._known_ow_state.used_ow_ids:
            raise OWStateMutationError(
                message="Cannot create ow object, already added as mutated state object.",
                action="add_mutated_ow",
                ow_object=ow_object.dict(),
            )
        # TODO: maybe add exception if mutating but no values changed? to prevent lvbb errors
        self._mutated_ow_objects.append(ow_object)

    def add_terminated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._known_ow_state.used_ow_ids:
            raise OWStateMutationError(
                message="Cannot terminate ow object as it did not exist in input state.",
                action="add_terminated_ow",
                ow_object=ow_object.dict(),
            )
        self._terminated_ow_objects.append(ow_object)

    # TODO: Refactor this block more efficiently when certain of mapping logic
    def get_new_locations(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, OWLocatie)]

    def get_mutated_locations(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, OWLocatie)]

    def get_terminated_locations(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, OWLocatie)]

    def get_new_div(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstdeel))]

    def get_mutated_div(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstdeel))]

    def get_terminated_div(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, (OWDivisie, OWDivisieTekst, OWTekstdeel))]

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
    def get_existing_gebied_id(self, werkingsgebied_code: str) -> Optional[str]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWGebied) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj.OW_ID
        return None

    def get_existing_gebiedengroep_id(self, werkingsgebied_code: str) -> Optional[str]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj.OW_ID
        return None

    def get_existing_ambtsgebied_id(self, uuid: UUID) -> Optional[str]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWAmbtsgebied) and ow_obj.mapped_uuid == uuid:
                return ow_obj.OW_ID
        return None

    def get_existing_regelingsgebied_id(self, ambtsgebied_ow_id: str) -> Optional[str]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWRegelingsgebied) and ow_obj.ambtsgebied == ambtsgebied_ow_id:
                return ow_obj.OW_ID
        return None

    def get_existing_divisie(self, wid: str) -> Optional[OWDivisieTekst]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWDivisieTekst) and ow_obj.wid == wid:
                return ow_obj
        return None

    def get_existing_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstdeel]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWTekstdeel) and ow_obj.divisie == divisie_ow_id:
                return ow_obj
        return None

    def get_existing_wid_list(self) -> List[str]:
        wid_list = []
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWDivisieTekst):
                wid_list.append(ow_obj.wid)
        return wid_list

    def get_existing_werkingsgebied_code_by_divisie(self, divisie_ow_id: str) -> Optional[str]:
        ow_tekstdeel = self.get_existing_tekstdeel_by_divisie(divisie_ow_id)
        if not ow_tekstdeel:
            return None

        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.OW_ID in ow_tekstdeel.locaties:
                return ow_obj.mapped_geo_code
        return None
