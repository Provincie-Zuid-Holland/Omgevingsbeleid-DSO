from copy import deepcopy
from typing import List, Optional

from ....services.ow.enums import OwProcedureStatus
from ....services.ow.ow_state_patcher import OWStatePatcher
from ....services.ow.ow_state_validator import OWStateValidator
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

    def _get_ow_procedure_status(self, soort_procedure: ProcedureType) -> Optional[OwProcedureStatus]:
        if soort_procedure == ProcedureType.Ontwerpbesluit:
            return OwProcedureStatus.ONTWERP
        elif soort_procedure == ProcedureType.Definitief_besluit:
            return None
        else:
            return None

    def apply(self, state_manager: StateManager) -> StateManager:
        provincie_id = state_manager.input_data.publication_settings.provincie_id
        levering_id = state_manager.input_data.publication_settings.opdracht.id_levering
        ow_procedure_status = self._get_ow_procedure_status(state_manager.input_data.besluit.soort_procedure)
        annotation_lookup_map = deepcopy(state_manager.act_ewid_service.get_state_object_tekst_lookup())
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()
        terminated_wids = self._find_terminated_wids(
            state_manager.input_data.get_known_wid_map(),
            state_manager.act_ewid_service.get_state_used_wid_map(),
            state_manager.ow_repository.get_existing_wid_list(),
        )

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
        # TODO: ensure empty files are not created for locaties / divisies
        ow_locatie_file = locatie_builder.create_file(locatie_template_data.dict())
        ow_manifest_builder.add_manifest_item(locatie_builder.FILE_NAME, locatie_template_data.object_type_list)
        state_manager.add_output_file(ow_locatie_file)

        ow_divisie_file = divisie_builder.create_file(divisie_template_data.dict())
        ow_manifest_builder.add_manifest_item(divisie_builder.FILE_NAME, divisie_template_data.object_type_list)
        state_manager.add_output_file(ow_divisie_file)

        if regelinggebied_builder.ambtsgebied:
            ow_regelingsgebied_file = regelinggebied_builder.create_file(regelingsgebied_template_data.dict())
            ow_manifest_builder.add_manifest_item(
                regelinggebied_builder.FILE_NAME, regelinggebied_builder.used_object_types
            )
            state_manager.add_output_file(ow_regelingsgebied_file)

        # manifest file builder runs last to only include used ow files.
        ow_manifest_template_data = ow_manifest_builder.build_template_data()
        ow_manifest_file = ow_manifest_builder.create_file(ow_manifest_template_data.dict())
        state_manager.add_output_file(ow_manifest_file)

        # Patch to get new ow data state
        ow_state_patcher = OWStatePatcher(
            ow_data=state_manager.input_data.ow_data.copy(deep=True),
            changed_ow_objects=state_manager.ow_repository.changed_ow_objects,
            terminated_ow_objects=state_manager.ow_repository.terminated_ow_objects,
        )
        ow_state_patcher.patch()

        # sanity check the patched state
        ow_state_validator = OWStateValidator(ow_data=ow_state_patcher.patched_ow_state)
        ow_state_validator.validate()

        state_manager.ow_object_state = ow_state_patcher.patched_ow_state

        return state_manager
