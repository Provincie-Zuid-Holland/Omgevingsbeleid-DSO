from typing import List

from ...services import BuilderService
from ...services.geo.gml_geometry_generator import GMLGeometryGenerator
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager
from ....models import ContentType
from ....services.utils.helpers import load_template


class GeoInformatieObjectVaststellingBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()

        for werkingsgebied in werkingsgebieden:
            output_file: OutputFile = self._generate_glm(werkingsgebied)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_glm(self, werkingsgebied: Werkingsgebied):
        locaties: List[dict] = []
        for location in werkingsgebied.Locaties:
            gml_id: str = f"gml-{location.UUID}"
            generator = GMLGeometryGenerator(
                gml_id,
                location.Geometry,
            )
            geometry_xml = generator.generate_xml()
            locaties.append(
                {
                    "gml_id": gml_id,
                    "groep_id": f"groep-{str(location.UUID)}",
                    "basis_id": str(location.UUID),
                    "naam": location.Title,
                    "geometry_xml": geometry_xml,
                }
            )

        content = load_template(
            "templates/geo/GeoInformatieObjectVaststelling.xml",
            pretty_print=True,
            achtergrondVerwijzing=werkingsgebied.Achtergrond_Verwijzing,
            achtergrondActualiteit=werkingsgebied.Achtergrond_Actualiteit,
            frbr=werkingsgebied.get_FRBR(),
            locaties=locaties,
        )

        output_file = OutputFile(
            filename=werkingsgebied.get_gml_filename(),
            content_type=ContentType.GML,
            content=StrContentData(content),
        )
        return output_file
