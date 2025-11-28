from typing import List

from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied

from ....models import ContentType
from ....services.utils.helpers import load_template
from ...builder_service import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class GeoInformatieObjectVaststellingBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        gebieden: List[Gebied] = state_manager.input_data.resources.gebied_repository.get_new()

        for gebied in gebieden:
            output_file: OutputFile = self._generate_glm(gebied)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_glm(self, gebied: Gebied):
        content = load_template(
            "geo/GeoInformatieObjectVaststelling.xml",
            pretty_print=True,
            gebied=gebied,
        )

        output_file = OutputFile(
            filename=gebied.get_gml_filename(),
            content_type=ContentType.GML,
            content=StrContentData(content),
        )
        return output_file
