from typing import List, Optional
from uuid import UUID

from ....models import OwData
from ....services.ow import (
    OWAmbtsgebied,
    OWDivisie,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OwLocatieObjectType,
    OWObject,
    OWRegelingsgebied,
    OWTekstDeel,
)
from ..exceptions import OWStateMutationError


class OWStateRepository:
    def __init__(self, ow_input_data: OwData) -> None:
        self._input_object_ids = ow_input_data.object_ids
        self._input_object_map = ow_input_data.object_map

        self._locaties_content = None
        self._divisie_content = None
        self._regelingsgebied_content = None

        self._new_ow_objects: List[OWObject] = []
        self._mutated_ow_objects: List[OWObject] = []
        self._terminated_ow_objects: List[OWObject] = []

    def add_new_ow(self, ow_object: OWObject) -> None:
        new_ow_id = ow_object.OW_ID
        if any(obj.OW_ID == new_ow_id for obj in self._new_ow_objects):
            raise OWStateMutationError(
                message="Cannot create owobject, already existing as new state object.",
                action="add_new_ow",
                ow_object=ow_object,
            )
        if any(obj.OW_ID == new_ow_id for obj in self._mutated_ow_objects):
            raise OWStateMutationError(
                message="Cannot create ow object: , already added as mutated state object.",
                action="add_new_ow",
                ow_object=ow_object,
            )
        self._new_ow_objects.append(ow_object)

    def add_mutated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._input_object_ids:
            raise OWStateMutationError(
                message="Cannot create ow object: already added as mutated state object.",
                action="add_mutated_ow",
                ow_object=ow_object,
            )
        # TODO: maybe add exception if mutating but no values changed? to prevent lvbb errors
        self._mutated_ow_objects.append(ow_object)

    def add_terminated_ow(self, ow_object: OWObject) -> None:
        if ow_object.OW_ID not in self._input_object_ids:
            raise OWStateMutationError(
                message="Cannot terminate ow object as it did not exist in input state.",
                action="add_terminated_ow",
                ow_object=ow_object,
            )
        self._terminated_ow_objects.append(ow_object)

    def get_changed_ow_objects(self) -> List[OWObject]:
        return self._new_ow_objects + self._mutated_ow_objects

    def get_gebiedengroep_by_code(self, werkingsgebied_code: str) -> Optional[OWGebiedenGroep]:
        # Search current state used objects
        for ow_obj in self.get_changed_ow_objects():
            if isinstance(ow_obj, OWGebiedenGroep) and ow_obj.mapped_geo_code == werkingsgebied_code:
                return ow_obj
        return None

    def get_active_ow_location_id(self, werkingsgebied_code: str) -> Optional[str]:
        # checks BOTH current state and input state for existing location id
        for obj in self.get_changed_ow_objects():
            if isinstance(obj, OWGebiedenGroep) and obj.mapped_geo_code == werkingsgebied_code:
                return obj.OW_ID

        return self.get_existing_gebiedengroep_id(werkingsgebied_code)

    def get_active_ambtsgebied_ow_id(self, ambtsgebied_uuid: UUID) -> Optional[str]:
        for obj in self.get_changed_ow_objects():
            if isinstance(obj, OWAmbtsgebied):
                return obj.OW_ID

        return self.get_existing_ambtsgebied_id(ambtsgebied_uuid)

    # fix
    def get_object_types(self):
        object_types = []
        for obj in self.get_changed_ow_objects() + self._terminated_ow_objects:
            if isinstance(obj, OWGebied):
                object_types.extend(OwLocatieObjectType.GEBIED.value)
            elif isinstance(obj, OWGebiedenGroep):
                object_types.extend(OwLocatieObjectType.GEBIEDENGROEP.value)
            elif isinstance(obj, OWAmbtsgebied):
                object_types.extend(OwLocatieObjectType.AMBTSGEBIED.value)
        return object_types

    #### INPUT STATE LOOKUPS ####

    def get_existing_gebied_id(self, werkingsgebied_code: str) -> Optional[str]:
        existing_id_map = self._input_object_map.get("id_mapping", None)
        gebied_map = existing_id_map.get("gebieden", {}) if existing_id_map else {}
        return gebied_map.get(werkingsgebied_code, None)

    def get_existing_gebiedengroep_id(self, werkingsgebied_code: str) -> Optional[str]:
        existing_id_map = self._input_object_map.get("id_mapping", None)
        gebiedengroep_map = existing_id_map.get("gebiedengroep", {}) if existing_id_map else {}
        return gebiedengroep_map.get(werkingsgebied_code, None)

    def get_existing_ambtsgebied_id(self, uuid: UUID) -> Optional[str]:
        existing_id_map = self._input_object_map.get("id_mapping", None)
        ambtsgebied_map = existing_id_map.get("ambtsgebied", {}) if existing_id_map else {}
        return ambtsgebied_map.get(str(uuid), None)

    def get_existing_divisie_id(self, wid: str) -> Optional[str]:
        existing_id_map = self._input_object_map.get("id_mapping", None)
        wid_map = existing_id_map.get("wid", {}) if existing_id_map else {}
        return wid_map.get(wid, None)

    def get_existing_tekstdeel_by_divisie(self, divisie_ow_id: str) -> Optional[OWTekstDeel]:
        existing_tekstdeel_map = self._input_object_map.get("tekstdeel_mapping", None)
        if not existing_tekstdeel_map:
            return None
        for tekstdeel_ow_id, values in existing_tekstdeel_map.items():
            if values["divisie"] == divisie_ow_id:
                return OWTekstDeel(OW_ID=tekstdeel_ow_id, locations=[values["location"]], divisie=divisie_ow_id)
        return None

    def get_existing_werkingsgebied_code_by_divisie(self, divisie_ow_id: str) -> Optional[str]:
        # ow_data state map could be changed to make these lookups less complex
        # for now we fetch the werkingsgebied-code <-> divisie_ow_id combination from the
        # previous state by backtracking the matching tekstdeel objects

        existing_id_map = self._input_object_map.get("id_mapping", None)
        ow_tekstdeel = self.get_existing_tekstdeel_by_divisie(divisie_ow_id) if existing_id_map else None

        if not existing_id_map or not ow_tekstdeel:
            return None

        for werkingsgebied_code, gebiedengroep_id in existing_id_map["gebiedengroep"].items():
            if gebiedengroep_id in ow_tekstdeel.locations:
                return werkingsgebied_code

        return None

    ######## OW STATE STORAGE - #TODO: rework ########

    def get_created_objects(self):
        created_ow_objects = []
        # Add locations
        keys = ["gebieden", "gebiedengroepen", "ambtsgebieden"]
        for key in keys:
            created_ow_objects.extend(self.locaties_content.get(key, []))

        # Add annotation sections
        annotations = self.divisie_content.get("annotaties", [])
        for annotation in annotations:
            attributes = [annotation.divisie_aanduiding, annotation.divisietekst_aanduiding, annotation.tekstdeel]
            created_ow_objects.extend(attr for attr in attributes if attr is not None)

        # ambtsgebied/regelingsgebied
        regelingsgebieden = self.regelingsgebied_content.get("regelingsgebieden")
        if regelingsgebieden:
            created_ow_objects.extend(regelingsgebieden)

        self.created_ow_objects = created_ow_objects
        return created_ow_objects

    def get_created_objects_id_list(self):
        ow_id_list = [ow.OW_ID for ow in self.created_ow_objects]
        return ow_id_list

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
                    "location": obj.locations[0],  # gebiedengroep
                }

        return created_ow_objects_map

    def store_locaties_content(self, xml_data):
        self.locaties_content = xml_data

    def store_divisie_content(self, xml_data):
        self.divisie_content = xml_data

    def store_regelingsgebied_content(self, xml_data):
        self.regelingsgebied_content = xml_data

    def get_location_objecttypes(self) -> List[Optional[str]]:
        return self.locaties_content.get("objectTypen", [])

    def get_divisie_objecttypes(self) -> List[Optional[str]]:
        return self.divisie_content.get("objectTypen", [])

    def get_regelingsgebied_objecttypes(self) -> List[Optional[str]]:
        return self.regelingsgebied_content.get("objectTypen", [])

    def to_dict(self):
        return {
            "locaties_content": self.locaties_content,
            "divisie_content": self.divisie_content,
            "regelingsgebied_content": self.regelingsgebied_content,
        }
