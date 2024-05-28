from copy import deepcopy
from typing import List, Optional


from ....services.ow.enums import OwProcedureStatus
from ....services.utils.waardelijsten import ProcedureType
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    """
    BuilderService that uses our previous state and the OWStateRepository to:
    - Handle any required OW object changes by running ow file builders
        for every file type (new, mutated, terminated).
    - Prepares the output template data and create each output file.
    - Patch a new ow data state.
    """

    def _find_terminated_wids(self, known_wid_map, current_wid_map, known_ow_wid_map) -> List[str]:
        """
        Compares the current wids used to the previous known state, to find objects that
        are no longer used and should be terminated.
        """
        removed_wids = []
        for obj_code, wid in known_wid_map.items():
            if obj_code not in current_wid_map and wid in known_ow_wid_map:
                removed_wids.append((obj_code, wid))

        terminated_wids: List[str] = [wid[1] for wid in removed_wids]
        # terminated_object_codes: List[str] = [wid[0] for wid in removed_wids]
        return terminated_wids

    def apply(self, state_manager: StateManager) -> StateManager:
        provincie_id = state_manager.input_data.publication_settings.provincie_id
        levering_id = state_manager.input_data.publication_settings.opdracht.id_levering
        ow_procedure_status: Optional[OwProcedureStatus] = None

        if state_manager.input_data.besluit.soort_procedure == ProcedureType.Ontwerpbesluit:
            ow_procedure_status = OwProcedureStatus.ONTWERP

        annotation_lookup_map = deepcopy(state_manager.ewid_service.get_state_object_tekst_lookup())
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()

        # compare wid maps to find policy objects that are not used anymore
        known_wid_map = state_manager.input_data.get_known_wid_map()
        used_wid_map = state_manager.ewid_service.get_state_used_wid_map()
        known_ow_wid_list = state_manager.ow_repository.get_existing_wid_list()
        terminated_wids = self._find_terminated_wids(known_wid_map, used_wid_map, known_ow_wid_list)

        # setup file builders
        locatie_builder = OwLocatieBuilder(
            provincie_id=provincie_id,
            levering_id=levering_id,
            ambtsgebied=state_manager.input_data.ambtsgebied,
            werkingsgebieden=werkingsgebieden,
            ow_repository=state_manager.ow_repository,
            ow_procedure_status=ow_procedure_status,
        )
        divisie_builder = OwDivisieBuilder(
            provincie_id=provincie_id,
            levering_id=levering_id,
            ow_repository=state_manager.ow_repository,
            annotation_lookup_map=annotation_lookup_map,
            terminated_wids=terminated_wids,
            ow_procedure_status=ow_procedure_status,
        )
        regelinggebied_builder = OwRegelingsgebiedBuilder(
            provincie_id=provincie_id,
            levering_id=levering_id,
            ow_procedure_status=ow_procedure_status,
            ow_repository=state_manager.ow_repository,
        )
        ow_manifest_builder = OwManifestBuilder(
            act=state_manager.input_data.publication_settings.regeling_frbr,
            doel=state_manager.input_data.publication_settings.instelling_doel.frbr,
        )

        # CRUD ow object
        locatie_builder.handle_ow_object_changes()
        divisie_builder.handle_ow_object_changes()
        regelinggebied_builder.handle_ow_object_changes()

        locatie_template_data = locatie_builder.build_template_data()
        divisie_template_data = divisie_builder.build_template_data()
        regelingsgebied_template_data = regelinggebied_builder.build_template_data()

        # create output files + owmanifest
        ow_locatie_file = locatie_builder.create_file(locatie_template_data.dict())
        ow_manifest_builder.add_manifest_item(locatie_builder.FILE_NAME, locatie_template_data.object_type_list)
        state_manager.add_output_file(ow_locatie_file)

        ow_divisie_file = divisie_builder.create_file(divisie_template_data.dict())
        ow_manifest_builder.add_manifest_item(divisie_builder.FILE_NAME, divisie_template_data.object_type_list)
        state_manager.add_output_file(ow_divisie_file)

        if regelinggebied_builder._ambtsgebied:
            ow_regelingsgebied_file = regelinggebied_builder.create_file(regelingsgebied_template_data.dict())
            ow_manifest_builder.add_manifest_item(
                regelinggebied_builder.FILE_NAME, regelinggebied_builder.object_type_list
            )
            state_manager.add_output_file(ow_regelingsgebied_file)

        # manifest file builder runs last to only include used ow files.
        ow_manifest_template_data = ow_manifest_builder.build_template_data()
        ow_manifest_file = ow_manifest_builder.create_file(ow_manifest_template_data.dict())
        state_manager.add_output_file(ow_manifest_file)

        # Set the result patched state
        state_manager.ow_object_state = state_manager.ow_repository.get_merged_ow_state()
        return state_manager
