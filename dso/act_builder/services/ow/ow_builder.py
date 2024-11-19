from typing import List

from ....services.ow.ow_state_patcher import OWStatePatcher
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder, OwFileBuilder
from ...services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from ...services.ow.ow_hoofdlijnen import OwHoofdlijnBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import OutputFile, StateManager


class OwBuilder(BuilderService):
    def __init__(
        self,
        locatie_builder: OwLocatieBuilder,
        divisie_builder: OwDivisieBuilder,
        gb_aanwijzing_builder: OwGebiedsaanwijzingBuilder,
        hoofdlijn_builder: OwHoofdlijnBuilder,
        regelinggebied_builder: OwRegelingsgebiedBuilder,
        ow_manifest_builder: OwManifestBuilder,
        ow_state_patcher: OWStatePatcher,
    ):
        self._ow_builders: List[OwFileBuilder] = [
            locatie_builder,
            divisie_builder,
            gb_aanwijzing_builder,
            hoofdlijn_builder,
            regelinggebied_builder,
        ]
        self._ow_manifest_builder = ow_manifest_builder
        self._ow_state_patcher = ow_state_patcher

    def apply(self, state_manager: StateManager) -> StateManager:
        """Handles OW object changes using the builders for each file, then patches the new ow state."""
        for builder in self._ow_builders:
            builder.handle_ow_object_changes()

        patched_ow_data = self._ow_state_patcher.patch(input_state_ow_data=state_manager.input_data.ow_data)
        state_manager.ow_object_state = patched_ow_data

        self._build_output_files(state_manager)

        return state_manager

    def _build_output_files(self, state_manager: StateManager) -> None:
        """Prepare the template data and create the output files for each ow file builder."""
        output_files: List[OutputFile] = []

        for builder in self._ow_builders:
            template_data = builder.build_template_data()
            if not template_data:
                continue  # only build files that have changed objs
            data_dict = template_data.dict()
            output_files.append(builder.create_file(template_data=data_dict))
            self._ow_manifest_builder.add_manifest_item(builder.FILE_NAME, template_data.object_type_list)

        ow_manifest_template_data = self._ow_manifest_builder.build_template_data()
        manifest_data = ow_manifest_template_data.dict()
        output_files.append(self._ow_manifest_builder.create_file(template_data=manifest_data))

        state_manager.add_output_files(output_files=output_files)
