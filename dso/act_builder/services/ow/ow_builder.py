from typing import List, Optional

from ....services.ow.enums import OwProcedureStatus
from ....services.ow.ow_state_patcher import OWStatePatcher
from ....services.utils.waardelijsten import ProcedureType
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager
from .ow_builder_context import BuilderContext


class OwBuilder(BuilderService):
    """
    BuilderService that uses our previous state and the OWStateRepository to:
    - Handle any required OW object changes by running ow file builders
        for every file type (new, mutated, terminated).
    - Prepares the output template data and create each output file.
    - Patch a new ow data state.
    """

    def apply(self, state_manager: StateManager) -> StateManager:
        orphaned_wids, orphaned_object_codes = self._calc_orphaned_wids(
            known_wid_map=state_manager.input_data.get_known_wid_map(),
            current_wid_map=state_manager.act_ewid_service.get_state_used_wid_map(),
            known_ow_wids=state_manager.ow_repository.get_existing_wid_list(),
        )

        # Create a shared context
        context = BuilderContext(
            provincie_id=state_manager.input_data.publication_settings.provincie_id,
            levering_id=state_manager.input_data.publication_settings.opdracht.id_levering,
            ow_procedure_status=self._get_ow_procedure_status(state_manager.input_data.besluit.soort_procedure),
            orphaned_wids=orphaned_wids,
            ow_repository=state_manager.ow_repository
        )

        # Pass the context to the builders
        locatie_builder = OwLocatieBuilder(
            context=context,
            werkingsgebieden=state_manager.input_data.resources.werkingsgebied_repository.all(),
            ambtsgebied=state_manager.input_data.ambtsgebied
        )
        divisie_builder = OwDivisieBuilder(
            context=context,
            annotation_lookup_map=state_manager.annotation_ref_lookup_map
        )
        gb_aanwijzing_builder = OwGebiedsaanwijzingBuilder(
            context=context,
            annotation_lookup_map=state_manager.annotation_ref_lookup_map
        )
        regelinggebied_builder = OwRegelingsgebiedBuilder(
            context=context
        )
        ow_manifest_builder = OwManifestBuilder(
            act=state_manager.input_data.publication_settings.regeling_frbr,
            doel=state_manager.input_data.publication_settings.instelling_doel.frbr
        )

        # CRUD ow object
        locatie_builder.handle_ow_object_changes()
        divisie_builder.handle_ow_object_changes()
        gb_aanwijzing_builder.handle_ow_object_changes()
        regelinggebied_builder.handle_ow_object_changes()

        # Patch to get new ow data state
        ow_state_patcher = OWStatePatcher(
            ow_data=state_manager.input_data.ow_data.copy(deep=True), ow_repository=state_manager.ow_repository
        )
        ow_state_patcher.patch()

        # Start building output files
        locatie_template_data = locatie_builder.build_template_data()
        divisie_template_data = divisie_builder.build_template_data()
        gebiedsaanwijzing_template_data = gb_aanwijzing_builder.build_template_data()
        regelingsgebied_template_data = regelinggebied_builder.build_template_data()

        # create output files + owmanifest
        if locatie_template_data:
            ow_locatie_file = locatie_builder.create_file(locatie_template_data.dict())
            ow_manifest_builder.add_manifest_item(locatie_builder.FILE_NAME, locatie_template_data.object_type_list)
            state_manager.add_output_file(ow_locatie_file)

        if divisie_template_data:
            ow_divisie_file = divisie_builder.create_file(divisie_template_data.dict())
            ow_manifest_builder.add_manifest_item(divisie_builder.FILE_NAME, divisie_template_data.object_type_list)
            state_manager.add_output_file(ow_divisie_file)

        if gebiedsaanwijzing_template_data:
            ow_gb_aanwijzing_file = gb_aanwijzing_builder.create_file(gebiedsaanwijzing_template_data.dict())
            ow_manifest_builder.add_manifest_item(
                gb_aanwijzing_builder.FILE_NAME, gebiedsaanwijzing_template_data.object_type_list
            )
            state_manager.add_output_file(ow_gb_aanwijzing_file)

        if regelinggebied_builder.get_ambtsgebied():
            ow_regelingsgebied_file = regelinggebied_builder.create_file(regelingsgebied_template_data.dict())
            ow_manifest_builder.add_manifest_item(
                regelinggebied_builder.FILE_NAME, regelinggebied_builder.get_used_object_types()
            )
            state_manager.add_output_file(ow_regelingsgebied_file)

        # manifest file builder runs last to only include used ow files.
        ow_manifest_template_data = ow_manifest_builder.build_template_data()
        ow_manifest_file = ow_manifest_builder.create_file(ow_manifest_template_data.dict())
        state_manager.add_output_file(ow_manifest_file)

        state_manager.ow_object_state = ow_state_patcher.get_patched_ow_state()

        return state_manager

    def _calc_orphaned_wids(self, known_wid_map, current_wid_map, known_ow_wids: List[str]):
        """
        Compares the current wids used to the previous known state, to find objects that
        are no longer used and should be considered as orphaned (no longer referenced in current state).
        """
        orphaned_wids = []
        orphaned_object_codes = []
        for obj_code, wid in known_wid_map.items():
            if obj_code not in current_wid_map and wid in known_ow_wids:
                orphaned_wids.append(wid)
                orphaned_object_codes.append(obj_code)

        return orphaned_wids, orphaned_object_codes

    def _get_ow_procedure_status(self, soort_procedure: ProcedureType) -> Optional[OwProcedureStatus]:
        """local helper to determine if ow objects should be created in concept modes"""
        match soort_procedure:
            case ProcedureType.Ontwerpbesluit:
                return OwProcedureStatus.ONTWERP
            case ProcedureType.Definitief_besluit:
                return None
            case _:
                return None
