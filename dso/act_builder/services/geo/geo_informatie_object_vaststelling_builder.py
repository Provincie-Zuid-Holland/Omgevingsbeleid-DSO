from typing import List

from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gio

from ....models import ContentType
from ....services.utils.helpers import load_template
from ...builder_service import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class GeoInformatieObjectVaststellingBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        gios: List[Gio] = state_manager.input_data.resources.gio_repository.get_new()

        for gio in gios:
            output_file: OutputFile = self._generate_glm(gio)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_glm(self, gio: Gio):
        content = load_template(
            "geo/GeoInformatieObjectVaststelling.xml",
            pretty_print=True,
            gio=gio,
        )

        output_file = OutputFile(
            filename=gio.get_gml_filename(),
            content_type=ContentType.GML,
            content=StrContentData(content),
        )
        return output_file
