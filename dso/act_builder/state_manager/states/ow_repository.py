import itertools
from typing import List, Optional, Union
from uuid import UUID

from ....models import OwData
from ....services.ow import (
    OWAmbtsgebied,
    OWDivisie,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWGebiedsaanwijzing,
    OWLocatie,
    OWObject,
    OWRegelingsgebied,
    OWTekstdeel,
)
from ..exceptions import OWObjectStateException, OWStateMutationError


class OWStateRepository:
    def __init__(self, ow_input_data: OwData) -> None:
        # Previous ow state from input
        self._known_ow_state = ow_input_data

        self._new_ow_objects: List[OWObject] = []
        self._mutated_ow_objects: List[OWObject] = []
        self._terminated_ow_objects: List[OWObject] = []

    def get_changed_ow_objects(self) -> List[OWObject]:
        """Changed == Actively used in the current state"""
        return self._new_ow_objects + self._mutated_ow_objects

    def get_terminated_ow_objects(self) -> List[OWObject]:
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
        # If ow_object OW_ID exists in known ow state and values are not
        # different from existing, # raise exception to prevent duplicate

        # existing_ow_object = self._known_ow_state.ow_objects[ow_object.OW_ID]
        # if existing_ow_object == ow_object:
        #     raise OWStateMutationError(
        #         message="Trying to add a mutated object to state with no changes, this would raise LVBB error.",
        #         action="add_mutated_ow",
        #         ow_object=ow_object.dict(),
        #     )
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

    def get_new_gebiedsaanwijzingen(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, OWGebiedsaanwijzing)]

    def get_mutated_gebiedsaanwijzingen(self) -> List[OWObject]:
        return [obj for obj in self._mutated_ow_objects if isinstance(obj, OWGebiedsaanwijzing)]

    def get_terminated_gebiedsaanwijzingen(self) -> List[OWObject]:
        return [obj for obj in self._terminated_ow_objects if isinstance(obj, OWGebiedsaanwijzing)]

    def get_new_tekstdeel(self) -> List[OWObject]:
        return [obj for obj in self._new_ow_objects if isinstance(obj, OWTekstdeel)]

    def get_gebiedengroep_by_code(self, werkingsgebied_code: str) -> Optional[OWGebiedenGroep]:
        # Search current state used objects
        for ow_obj in self.get_changed_ow_objects():
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_new_ambtsgebied(self) -> Optional[OWAmbtsgebied]:
        for ow_obj in self._new_ow_objects:
            if isinstance(ow_obj, OWAmbtsgebied):
                return ow_obj
        return None

    def get_divisie_by_wid(self, wid: str) -> Optional[Union[OWDivisie, OWDivisieTekst]]:
        for ow_obj in self.get_changed_ow_objects():
            if isinstance(ow_obj, OWDivisieTekst) and ow_obj.wid == wid:
                return ow_obj
        return None

    def get_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstdeel]:
        for ow_obj in self.get_changed_ow_objects():
            if isinstance(ow_obj, OWTekstdeel) and ow_obj.divisie == divisie_ow_id:
                return ow_obj
        return None

    def update_state_tekstdeel(self, state_ow_id: str, updated_obj: OWTekstdeel) -> None:
        for idx, ow_obj in enumerate(self._new_ow_objects):
            if ow_obj.OW_ID == state_ow_id:
                self._new_ow_objects[idx] = updated_obj
                return
        for idx, ow_obj in enumerate(self._mutated_ow_objects):
            if ow_obj.OW_ID == state_ow_id:
                self._mutated_ow_objects[idx] = updated_obj
                return

        raise OWStateMutationError(
            message="Cannot update tekstdeel, not found in new or mutated state list.",
            action="update_state_tekstdeel",
            ow_object=updated_obj.dict(),
        )

    def get_gebiedsaanwijzing_by_wid(self, wid: str) -> Optional[OWGebiedsaanwijzing]:
        for ow_obj in self.get_changed_ow_objects():
            if isinstance(ow_obj, OWGebiedsaanwijzing) and ow_obj.wid == wid:
                return ow_obj
        return None

    # active state lookups return either new/mutated or known state objects
    def get_active_div_by_wid(self, wid: str) -> Optional[Union[OWDivisie, OWDivisieTekst]]:
        ow_objects = itertools.chain(self.get_changed_ow_objects(), self._known_ow_state.ow_objects.values())
        return next(
            (ow_obj for ow_obj in ow_objects if isinstance(ow_obj, (OWDivisie, OWDivisieTekst)) and ow_obj.wid == wid),
            None,
        )

    def get_active_tekstdeel_by_div(self, divisie_ow_id: str) -> Optional[OWTekstdeel]:
        ow_objects = itertools.chain(self.get_changed_ow_objects(), self._known_ow_state.ow_objects.values())
        return next(
            (ow_obj for ow_obj in ow_objects if isinstance(ow_obj, OWTekstdeel) and ow_obj.divisie == divisie_ow_id),
            None,
        )

    def get_active_gebiedengroep_by_code(self, werkingsgebied_code: str) -> Optional[OWGebiedenGroep]:
        # first check changed state objects, then existing state objects
        active_gebiedengroep = self.get_gebiedengroep_by_code(werkingsgebied_code)
        if not active_gebiedengroep:
            active_gebiedengroep = self.get_known_gebiedengroep_by_code(werkingsgebied_code)

        return active_gebiedengroep

    # KNOWN STATE MAP LOOKUPS
    def get_known_state_object(self, ow_id: str) -> Optional[OWObject]:
        return self._known_ow_state.ow_objects.get(ow_id, None)

    def get_known_gebied_by_code(self, werkingsgebied_code: str) -> Optional[OWGebied]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWGebied) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_known_gebiedengroep_by_code(self, werkingsgebied_code: str) -> Optional[OWGebiedenGroep]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_existing_gebiedengroep(self, ow_id: str) -> OWGebiedenGroep:
        ow_obj = self._known_ow_state.ow_objects.get(ow_id, None)
        if not ow_obj or not isinstance(ow_obj, OWGebiedenGroep):
            raise OWObjectStateException(
                message=f"Expected OWGebiedenGroep type object in existing state OW_ID: {ow_id}.",
                ref_ow_id=ow_id,
            )
        return ow_obj

    def get_existing_locatie(self, ow_id: str) -> Union[OWGebied, OWGebiedenGroep]:
        ow_obj = self._known_ow_state.ow_objects.get(ow_id, None)
        if not ow_obj or not isinstance(ow_obj, (OWGebied, OWGebiedenGroep)):
            raise OWObjectStateException(
                message=f"Expected OWGebied or OWGebiedenGroep type object in existing state OW_ID: {ow_id}.",
                ref_ow_id=ow_id,
            )
        return ow_obj

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

    def get_existing_regelingsgebied(self) -> Optional[OWRegelingsgebied]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWRegelingsgebied):
                return ow_obj
        return None

    def get_existing_divisie(self, wid: str) -> Optional[Union[OWDivisie, OWDivisieTekst]]:
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, (OWDivisie, OWDivisieTekst)) and ow_obj.wid == wid:
                return ow_obj
        return None

    def get_existing_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstdeel]:
        if divisie_ow_id not in self._known_ow_state.used_ow_ids:
            return None

        return next(
            (
                ow_obj
                for ow_obj in self._known_ow_state.ow_objects.values()
                if isinstance(ow_obj, OWTekstdeel) and ow_obj.divisie == divisie_ow_id
            )
        )

    def get_existing_wid_list(self) -> List[str]:
        wid_list = []
        for ow_obj in self._known_ow_state.ow_objects.values():
            if isinstance(ow_obj, OWDivisie):
                wid_list.append(ow_obj.wid)
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
