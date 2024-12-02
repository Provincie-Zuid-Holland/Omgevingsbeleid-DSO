from typing import List

from ....models import ContentType
from ....services.utils.helpers import load_template
from ...services import BuilderService
from ...services.geo.gml_geometry_generator import GMLGeometryGenerator
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Locatie, Werkingsgebied
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class GeoInformatieObjectVaststellingBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()

        for werkingsgebied in werkingsgebieden:
            if werkingsgebied.New:
                output_file: OutputFile = self._generate_glm(werkingsgebied)
                state_manager.add_output_file(output_file)

        return state_manager

    def _generate_glm(self, werkingsgebied: Werkingsgebied):
        locaties: List[dict] = []
        for location in werkingsgebied.Locaties:
            geometry_xml = self._get_geometry_xml(location.Gml_ID, location)
            locaties.append(
                {
                    "gml_id": location.Gml_ID,
                    "groep_id": location.Group_ID,
                    "basis_id": location.Identifier,
                    "naam": location.Title,
                    "geometry_xml": geometry_xml,
                }
            )

        content = load_template(
            "geo/GeoInformatieObjectVaststelling.xml",
            pretty_print=True,
            achtergrondVerwijzing=werkingsgebied.Achtergrond_Verwijzing,
            achtergrondActualiteit=werkingsgebied.Achtergrond_Actualiteit,
            frbr=werkingsgebied.Frbr,
            locaties=locaties,
        )

        output_file = OutputFile(
            filename=werkingsgebied.get_gml_filename(),
            content_type=ContentType.GML,
            content=StrContentData(content),
        )
        return output_file

    def _get_geometry_xml(self, gml_id: str, location: Locatie) -> str:
        if location.Gml is not None:
            return location.Gml
        elif location.Geometry is not None:
            generator = GMLGeometryGenerator(
                gml_id,
                location.Geometry,
            )
            geometry_xml = generator.generate_xml()
            return geometry_xml

        raise RuntimeError("Should have a Gml or Geometry for Location")
