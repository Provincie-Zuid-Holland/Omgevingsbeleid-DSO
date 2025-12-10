from typing import List
from dso.act_builder.state_manager.input_data.resource.gebieden.types import GeoGio
from ....models import ContentType
from ....services.utils.hashlib import compute_sha512_of_output_file
from ....services.utils.helpers import load_template
from ...builder_service import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class GioAanleveringInformatieObjectBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        gios: List[GeoGio] = state_manager.input_data.resources.geogio_repository.get_new()

        for gio in gios:
            output_file: OutputFile = self._generate_gio_file(state_manager, gio)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_gio_file(
        self,
        state_manager: StateManager,
        gio: GeoGio,
    ):
        gml_filename = gio.get_gml_filename()
        output_file = state_manager.get_output_file_by_filename(gml_filename)
        gml_hash = compute_sha512_of_output_file(output_file)

        content = load_template(
            "geo/AanleveringInformatieObject.xml",
            pretty_print=True,
            gio=gio,
            gml_hash=gml_hash,
            provincie_ref=state_manager.input_data.publication_settings.provincie_ref,
        )

        output_file = OutputFile(
            filename=gio.get_gio_filename(),
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
