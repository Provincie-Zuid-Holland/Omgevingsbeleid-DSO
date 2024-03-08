from typing import List, Optional
from uuid import UUID

from ....models import ContentType
from ....services.ow.enums import IMOWTYPES, OwLocatieObjectType, OwProcedureStatus
from ....services.ow.models import OWAmbtsgebied, OWGebied, OWGebiedenGroep
from ....services.ow.ow_id import generate_ow_id
from ....services.utils.helpers import load_template
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ...state_manager.models import OutputFile, StrContentData


class OwLocatiesContent:
    """
    Prepares the content for the OWLocaties file from Werkingsgebieden.

    Assuming that ambtsgebied should only be defined as location
    on the first publication or if updated in value based on TPOD 2.0.2
    https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20230407/#00B96535
    """

    def __init__(
        self,
        werkingsgebieden: List[Werkingsgebied],
        object_tekst_lookup: dict,
        levering_id: str,
        ow_procedure_status: OwProcedureStatus,
        ambtsgebied_data: Optional[dict],
    ):
        self.werkingsgebieden = werkingsgebieden
        self.object_tekst_lookup = object_tekst_lookup
        self.levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self.ambtsgebied_data = ambtsgebied_data

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

        if self.ambtsgebied_data:
            ambtsgebied = self._create_amtsgebied(self.ambtsgebied_data)
            self.xml_data["ambtsgebieden"].append(ambtsgebied)

        self._add_object_types()
        self.file = self.create_file()
        return self.xml_data

    def _create_ow_locations(self):
        """
        Create new OW Locations from werkingsgebieden.
        Use manual ambtsgebied for now.
        """
        for werkingsgebied in self.werkingsgebieden:
            ow_locations = [
                OWGebied(
                    OW_ID=generate_ow_id(ow_type=IMOWTYPES.GEBIED, unique_code=loc.UUID.hex),
                    geo_uuid=loc.UUID,
                    noemer=loc.Title,
                    procedure_status=self.ow_procedure_status,
                )
                for loc in werkingsgebied.Locaties
            ]
            ow_group = OWGebiedenGroep(
                OW_ID=generate_ow_id(ow_type=IMOWTYPES.GEBIEDENGROEP, unique_code=werkingsgebied.UUID.hex),
                geo_uuid=werkingsgebied.UUID,
                noemer=werkingsgebied.Title,
                locations=ow_locations,
                procedure_status=self.ow_procedure_status,
            )
            self.xml_data["gebieden"].extend(ow_locations)
            self.xml_data["gebiedengroepen"].append(ow_group)

        # Update object_tekst_lookup with OW_IDs
        ow_gebied_mapping = {gebied.geo_uuid: gebied.OW_ID for gebied in self.xml_data["gebieden"]}
        ow_gebied_mapping.update(
            {gebiedengroep.geo_uuid: gebiedengroep.OW_ID for gebiedengroep in self.xml_data["gebiedengroepen"]}
        )
        for object_code, values in self.object_tekst_lookup.items():
            if values.get("gebied_uuid", None) is None:
                continue
            # Find the matching OWGebied and update ow_location_id to the state
            matching_ow_gebied = ow_gebied_mapping.get(UUID(values["gebied_uuid"]))
            if matching_ow_gebied:
                values["ow_location_id"] = matching_ow_gebied

    def _create_amtsgebied(self, ambtsgebied_data: dict):
        """
        Should only create an ambtsgebied if manually added or updated.
        """
        new_ambtsgebied = OWAmbtsgebied(**ambtsgebied_data)
        new_ambtsgebied.procedure_status = self.ow_procedure_status
        return new_ambtsgebied

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
            "ow/owLocaties.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owLocaties.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
