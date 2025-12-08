from typing import List
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied
from ....models import ContentType
from ....services.utils.hashlib import compute_sha512_of_output_file
from ....services.utils.helpers import load_template
from ...builder_service import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class GioAanleveringInformatieObjectBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        gebieden: List[Gebied] = state_manager.input_data.resources.gebied_repository.get_new()

        for gebied in gebieden:
            output_file: OutputFile = self._generate_gio(state_manager, gebied)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_gio(
        self,
        state_manager: StateManager,
        gebied: Gebied,
    ):
        gml_filename = gebied.get_gml_filename()
        output_file = state_manager.get_output_file_by_filename(gml_filename)
        gml_hash = compute_sha512_of_output_file(output_file)

        content = load_template(
            "geo/AanleveringInformatieObject.xml",
            pretty_print=True,
            gebied_frbr=gebied.frbr,
            bestandsnaam=gebied.get_gml_filename(),
            gml_hash=gml_hash,
            geboorteregeling=gebied.geboorteregeling,
            provincie_ref=state_manager.input_data.publication_settings.provincie_ref,
            naamInformatie_object=gebied.title,
        )

        output_file = OutputFile(
            filename=gebied.get_gio_filename(),
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
