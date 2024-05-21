from typing import List, Optional, Type
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
    OWTekstDeel,
)
from ..exceptions import OWStateMutationError


class OWRepository:
    def __init__(self, ow_input_data: OwData) -> None:
        self._known_object_ids = ow_input_data.object_ids
        self._known_object_map = ow_input_data.object_map

        self._locaties_content = None
        self._divisie_content = None
        self._regelingsgebied_content = None

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
        if ow_object.OW_ID not in self._known_object_ids:
            raise OWStateMutationError(
                message="Cannot create ow object, already added as mutated state object.",
                action="add_mutated_ow",
                ow_object=ow_object,
            )
        # TODO: maybe add exception if mutating but no values changed? to prevent lvbb errors
        self._mutated_ow_objects.append(ow_object)

    def add_terminated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._known_object_ids:
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

    ### KNOWN STATE LOOKUPS ####
    def get_existing_gebied_id(self, werkingsgebied_code: str) -> Optional[str]:
        gebied_map = self._known_object_map.id_mapping.gebieden
        return gebied_map.get(werkingsgebied_code, None)

    def get_existing_gebiedengroep_id(self, werkingsgebied_code: str) -> Optional[str]:
        gebiedengroep_map = self._known_object_map.id_mapping.gebiedengroep
        return gebiedengroep_map.get(werkingsgebied_code, None)

    def get_existing_ambtsgebied_id(self, uuid: UUID) -> Optional[str]:
        ambtsgebied_map = self._known_object_map.id_mapping.ambtsgebied
        return ambtsgebied_map.get(str(uuid), None)

    def get_existing_regelingsgebied_id(self, ambtsgebied_ow_id: str) -> Optional[str]:
        regelingsgebied_map = self._known_object_map.id_mapping.regelingsgebied
        return regelingsgebied_map.get(ambtsgebied_ow_id, None)

    def get_existing_divisie(self, wid: str) -> Optional[OWDivisieTekst]:
        wid_map = self._known_object_map.id_mapping.wid
        ow_divisie_id = wid_map.get(wid, None)
        return OWDivisieTekst(OW_ID=ow_divisie_id, wid=wid) if ow_divisie_id else None

    def get_existing_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstDeel]:
        existing_tekstdeel_map = self._known_object_map.tekstdeel_mapping
        for tekstdeel_ow_id, values in existing_tekstdeel_map.items():
            if values.divisie == divisie_ow_id:
                return OWTekstDeel(OW_ID=tekstdeel_ow_id, locaties=[values.location], divisie=divisie_ow_id)
        return None

    def get_existing_wid_list(self) -> List[str]:
        existing_id_map = self._known_object_map.id_mapping
        wid_map = existing_id_map.wid
        return list(wid_map.keys())

    def get_existing_werkingsgebied_code_by_divisie(self, divisie_ow_id: str) -> Optional[str]:
        # ow_data state map could be changed to make these lookups less complex
        # for now we fetch the werkingsgebied-code <-> divisie_ow_id combination from the
        # previous state by backtracking the matching tekstdeel objects
        existing_id_map = self._known_object_map.id_mapping
        ow_tekstdeel = self.get_existing_tekstdeel_by_divisie(divisie_ow_id)

        if not existing_id_map or not ow_tekstdeel:
            return None

        for werkingsgebied_code, gebiedengroep_id in existing_id_map.gebiedengroep.items():
            if gebiedengroep_id in ow_tekstdeel.locaties:
                return werkingsgebied_code

        return None

    ######## OW STATE MAPPING - #TODO: rework ########

    def get_ow_object_mapping(self):
        # Mapping of created OW IDS to input identifiers for export state reference
        created_ow_objects_map = {
            "id_mapping": {
                "gebieden": {},
                "gebiedengroep": {},
                "ambtsgebied": {},
                "wid": {},
                "regelingsgebied": {},
            },
            "tekstdeel_mapping": {},
        }

        for obj in self.created_ow_objects:
            if isinstance(obj, OWGebied):
                created_ow_objects_map["id_mapping"]["gebieden"][obj.mapped_geo_code] = obj.OW_ID
            if isinstance(obj, OWGebiedenGroep):
                created_ow_objects_map["id_mapping"]["gebiedengroep"][obj.mapped_geo_code] = obj.OW_ID
            if isinstance(obj, OWDivisie) or isinstance(obj, OWDivisieTekst):
                created_ow_objects_map["id_mapping"]["wid"][obj.wid] = obj.OW_ID
            if isinstance(obj, OWAmbtsgebied):
                created_ow_objects_map["id_mapping"]["ambtsgebied"][str(obj.mapped_uuid)] = obj.OW_ID
            if isinstance(obj, OWRegelingsgebied):
                created_ow_objects_map["id_mapping"]["regelingsgebied"][obj.ambtsgebied] = obj.OW_ID
            if isinstance(obj, OWTekstDeel):
                created_ow_objects_map["tekstdeel_mapping"][obj.OW_ID] = {
                    "divisie": obj.divisie,
                    "location": obj.locaties[0],  # gebiedengroep
                }

        return created_ow_objects_map

    def store_locaties_content(self, xml_data):
        self.locaties_content = xml_data

    def store_divisie_content(self, xml_data):
        self.divisie_content = xml_data

    def store_regelingsgebied_content(self, xml_data):
        self.regelingsgebied_content = xml_data
