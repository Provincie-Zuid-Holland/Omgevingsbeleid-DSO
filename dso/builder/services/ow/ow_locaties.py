from typing import List
from uuid import UUID

from dso.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from dso.builder.state_manager.models import OutputFile, StrContentData
from dso.models import ContentType
from dso.services.ow.enums import OwLocatieObjectType
from dso.services.ow.models import BestuurlijkeGrenzenVerwijzing, OWAmbtsgebied, OWGebied, OWGebiedenGroep
from dso.services.utils.helpers import load_template


class OwLocatiesContent:
    """
    Prepares the content for the OWLocaties file from Werkingsgebieden.
    """

    def __init__(self, werkingsgebieden: List[Werkingsgebied], object_tekst_lookup, levering_id):
        self.werkingsgebieden = werkingsgebieden
        self.object_tekst_lookup = object_tekst_lookup
        self.levering_id = levering_id
        self.xml_data = {
            "filename": "owLocaties.xml",
            "leveringsId": self.levering_id,
            "objectTypen": [],
            "gebiedengroepen": [],
            "gebieden": [],
            "ambtsgebieden": [],
        }
        self.file = None

    def create_locations(self):
        """
        Create OWGebied and OWGebiedenGroep objects and return them in a dict
        """
        self._create_ow_locations()
        self._add_object_types()
        self.file = self.create_file()
        return self.xml_data

    def _create_ow_locations(self):
        """
        Create new OW Locations from werkingsgebieden.
        Use manual ambtsgebied for now.
        """

        for werkingsgebied in self.werkingsgebieden:
            ow_locations = [OWGebied(geo_uuid=loc.UUID, noemer=loc.Title) for loc in werkingsgebied.Locaties]
            ow_group = OWGebiedenGroep(
                geo_uuid=werkingsgebied.UUID,
                noemer=werkingsgebied.Title,
                locations=ow_locations,
            )
            self.xml_data["gebieden"].extend(ow_locations)
            self.xml_data["gebiedengroepen"].append(ow_group)

        # Manually add ambtsgebied
        ambtsgebied = OWAmbtsgebied(
            OW_ID="nl.imow-pv28.ambtsgebied.002000000000000000009928",
            bestuurlijke_genzenverwijzing=BestuurlijkeGrenzenVerwijzing(
                bestuurlijke_grenzen_id="PV28",
                domein="NL.BI.BestuurlijkGebied",
                geldig_op="2023-09-29",
            ),
        )
        self.xml_data["ambtsgebieden"].append(ambtsgebied)

        # Update object_tekst_lookup with OW_IDs
        ow_gebied_mapping = {gebied.geo_uuid: gebied.OW_ID for gebied in self.xml_data["gebieden"]}
        ow_gebied_mapping.update(
            {gebiedengroep.geo_uuid: gebiedengroep.OW_ID for gebiedengroep in self.xml_data["gebiedengroepen"]}
        )
        for object_code, values in self.object_tekst_lookup.items():
            # Find the matching OWGebied and update ow_location_id to the state
            matching_ow_gebied = ow_gebied_mapping.get(UUID(values["gebied_uuid"]))
            if matching_ow_gebied:
                values["ow_location_id"] = matching_ow_gebied

    def _add_object_types(self):
        # Add object types for used location types
        if len(self.xml_data["gebieden"]) > 0:
            self.xml_data["objectTypen"].append(OwLocatieObjectType.GEBIED.value)
        if len(self.xml_data["gebiedengroepen"]) > 0:
            self.xml_data["objectTypen"].append(OwLocatieObjectType.GEBIEDENGROEP.value)
        if len(self.xml_data["ambtsgebieden"]) > 0:
            self.xml_data["objectTypen"].append(OwLocatieObjectType.AMBTSGEBIED.value)

    def create_file(self):
        content = load_template(
            "templates/ow/owLocaties.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owLocaties.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
