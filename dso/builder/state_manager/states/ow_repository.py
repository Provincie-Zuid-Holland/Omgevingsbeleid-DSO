from typing import List, Optional

from ....services.ow.models import OWDivisie, OWDivisieTekst, OWGebied, OWGebiedenGroep


class OWStateRepository:
    """
    A class that represents the state repository for OW objects.

    Attributes:
        locaties_content (dict): The content of the locaties XML data.
        divisie_content (dict): The content of the divisie XML data.
        regelingsgebied_content (dict): The content of the regelingsgebied XML data.
        created_ow_objects (list): The created OW objects.
    """

    def __init__(self):
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
        """
        Mapping of created OW IDS to input identifiers for export state reference
        """
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
        """
        Stores the locaties XML data.

        Args:
            xml_data (dict): The locaties XML data.
        """
        self.locaties_content = xml_data

    def store_divisie_content(self, xml_data):
        """
        Stores the divisie XML data.

        Args:
            xml_data (dict): The divisie XML data.
        """
        self.divisie_content = xml_data

    def store_regelingsgebied_content(self, xml_data):
        """
        Stores the regelingsgebied XML data.

        Args:
            xml_data (dict): The regelingsgebied XML data.
        """
        self.regelingsgebied_content = xml_data

    def get_location_objecttypes(self) -> List[Optional[str]]:
        """
        Retrieves the object types from the locaties content.

        Returns:
            list: The object types from the locaties content.
        """
        return self.locaties_content.get("objectTypen", [])

    def get_divisie_objecttypes(self) -> List[Optional[str]]:
        """
        Retrieves the object types from the divisie content.

        Returns:
            list: The object types from the divisie content.
        """
        return self.divisie_content.get("objectTypen", [])

    def get_regelingsgebied_objecttypes(self) -> List[Optional[str]]:
        """
        Retrieves the object types from regelingsgebied content.

        Returns:
            list: The object types from regelingsgebied content.
        """
        return self.regelingsgebied_content.get("objectTypen", [])

    def to_dict(self):
        """
        Converts the OW state repository to a dictionary.

        Returns:
            dict: The OW state repository as a dictionary.
        """
        return {
            "locaties_content": self.locaties_content,
            "divisie_content": self.divisie_content,
            "regelingsgebied_content": self.regelingsgebied_content,
        }
