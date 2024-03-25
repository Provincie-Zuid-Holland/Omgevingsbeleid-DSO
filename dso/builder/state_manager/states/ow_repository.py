from typing import Dict, List, Optional

from ....models import OwData
from ....services.ow.models import OWDivisie, OWDivisieTekst, OWGebied, OWGebiedenGroep


class OWStateRepository:
    def __init__(self, ow_input_data: OwData):
        self._input_object_ids: List[str] = ow_input_data.object_ids
        self._input_object_map: Dict[str, Dict[str, str]] = ow_input_data.object_map

        self.locaties_content = None
        self.divisie_content = None
        self.regelingsgebied_content = None

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

        # ambtsgebied/regelingsgebied? excluded for now
        return created_ow_objects

    def get_created_objects_id_list(self):
        created_ow_objects = self.get_created_objects()
        ow_id_list = [ow.OW_ID for ow in created_ow_objects]
        return ow_id_list

    def get_ow_object_mapping(self):
        # Mapping of created OW IDS to input identifiers for export state reference
        created_ow_objects = self.get_created_objects()
        created_ow_objects_map = {
            "gebieden_map": {},
            "gebiedengroep_map": {},
            "wid_map": {},
        }

        for obj in created_ow_objects:
            if isinstance(obj, OWGebied):
                created_ow_objects_map["gebieden_map"][obj.mapped_geo_code] = obj.OW_ID
            if isinstance(obj, OWGebiedenGroep):
                created_ow_objects_map["gebiedengroep_map"][obj.mapped_geo_code] = obj.OW_ID
            if isinstance(obj, OWDivisie) or isinstance(obj, OWDivisieTekst):
                created_ow_objects_map["wid_map"][obj.wid] = obj.OW_ID

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
