from copy import deepcopy
from typing import List, Optional, Tuple

from ....services.ow.enums import OwProcedureStatus
from ....services.utils.waardelijsten import ProcedureType
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import ManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    """
    TODO:
    - Add 'last step state validation/cleanup' ow_repository that checks the lvvb rules:
        - No isolated/dangling objects,
        - No werkingsgebied_code with multiple gebiedgroep / gebied objects in reference
        - other OW specific rules etc.
    - If validation is false due to dangling OW objects
        - Add terminate dangling IDs (all content is needed or partial is okay?)
    - Make OWstate typed
    - Merge old input ow state with new and rewrite the owstate export to not so horrible
    - Ambtsgebied object mutations low prio but should work anyways
    """

    def apply(self, state_manager: StateManager) -> StateManager:
        provincie_id: str = state_manager.input_data.publication_settings.provincie_id
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

        terminated_object_wids = self.find_terminated_wids(known_wid_map, used_wid_map, known_ow_wid_list)
        terminated_wids: List[str] = [wid[1] for wid in terminated_object_wids]
        terminated_object_codes: List[str] = [wid[0] for wid in terminated_object_wids]
        # terminated_werkingsgebieden = [wid for wid in terminated_wids if wid[0] == "werkingsgebied"]

        locatie_builder = OwLocatieBuilder(
            provincie_id=provincie_id,
            levering_id=levering_id,
            ambtsgebied=state_manager.input_data.ambtsgebied,
            werkingsgebieden=werkingsgebieden,
            ow_repository=state_manager.ow_repository,
            ow_procedure_status=ow_procedure_status,
        )
        # updates OW state for werkingsgebieden
        locatie_builder.handle_ow_object_changes()

        # updates OW state for text section annotations
        divisie_builder = OwDivisieBuilder(
            provincie_id=provincie_id,
            levering_id=levering_id,
            ow_repository=state_manager.ow_repository,
            annotation_lookup_map=annotation_lookup_map,
            terminated_wids=terminated_wids,
            ow_procedure_status=ow_procedure_status,
        )
        divisie_builder.handle_ow_object_changes()

        # changed_ambtsgebied = state_manager.ow_repository.get_changed_ambtsgebied()
        # if changed_ambtsgebied:
        #     regelinggebied_builder = OwRegelingsgebiedBuilder(
        #         provincie_id=provincie_id,
        #         ow_procedure_status=ow_procedure_status,
        #         ow_repository=state_manager.ow_repository,
        #         ambtsgebied_ow_id=changed_ambtsgebied.OW_ID,
        #     )
        #     regelinggebied_builder.handle_ow_object_changes()

        # get all locatie ow objects pending for output
        # state_manager.created_ow_object_ids = state_manager.ow_repository.get_created_objects_id_list()
        # state_manager.created_ow_objects_map = state_manager.ow_repository.get_ow_object_mapping()

        # ow_manifest_builder = ManifestBuilder(
        #     act_work=str(state_manager.input_data.publication_settings.regeling_frbr.get_work()),
        #     doel=state_manager.input_data.publication_settings.instelling_doel.frbr,
        # )
        # ow_manifest_builder.create_manifest(
        #     state_manager.ow_repository.divisie_content,
        #     state_manager.ow_repository.locaties_content,
        #     state_manager.ow_repository.regelingsgebied_content,
        # )

        # create files
        locatie_file_data = locatie_builder.build_file_data()
        ow_locatie_file = locatie_builder.create_file(locatie_file_data)

        divisie_file_data = divisie_builder.build_file_data()
        ow_divisie_file = divisie_builder.create_file(divisie_file_data)

        # regelingsgbied
        # manifest

        # store created files
        state_manager.add_output_files([ow_locatie_file, ow_divisie_file])

        return state_manager

    def find_terminated_wids(self, known_wid_map, current_wid_map, known_ow_wid_map) -> List[Tuple[str, str]]:
        """
        Compares the current wids used to the previous known state, to find objects that
        are no longer used and should be terminated.
        """
        removed_wids = []
        for obj_code, wid in known_wid_map.items():
            if obj_code not in current_wid_map and wid in known_ow_wid_map:
                removed_wids.append((obj_code, wid))
        return removed_wids
