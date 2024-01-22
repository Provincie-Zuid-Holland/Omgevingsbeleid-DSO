from typing import List, Optional


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
        self.created_ow_objects = []

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

    def store_created_ow_object(self, ow_object):
        """
        Add new created OW object to the state.

        Args:
            ow_object (OWObject): The OW object to add to the state.
        """
        self.created_ow_objects.append(ow_object)

    def get_created_ow_objects(self):
        """
        Retrieves the created OW objects.

        Returns:
            list: The created OW objects.
        """
        return self.created_ow_objects

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