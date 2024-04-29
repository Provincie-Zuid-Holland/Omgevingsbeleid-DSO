from copy import deepcopy
from typing import Optional

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
        leveringid = state_manager.input_data.publication_settings.opdracht.id_levering
        ow_procedure_status: Optional[OwProcedureStatus] = None

        if state_manager.input_data.besluit.soort_procedure == ProcedureType.Ontwerpbesluit:
            ow_procedure_status = OwProcedureStatus.ONTWERP

        annotation_lookup_map = deepcopy(state_manager.ewid_service.get_state_object_tekst_lookup())
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()

        locatie_builder = OwLocatieBuilder(
            provincie_id=provincie_id,
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
            ow_repository=state_manager.ow_repository,
            annotation_lookup_map=annotation_lookup_map,
            ow_procedure_status=ow_procedure_status,
        )
        divisie_state = divisie_builder.handle_divisie_changes()

        # TODO: for new version ensure if no new ambtsgebied created, same regelingsgebied is used
        ambtsgebied_id = state_manager.ow_repository.get_active_ambtsgebied_ow_id(
            ambtsgebied_uuid=state_manager.input_data.ambtsgebied.UUID
        )
        regelinggebied_builder = OwRegelingsgebiedBuilder(
            provincie_id=provincie_id,
            levering_id=leveringid,
            ow_procedure_status=ow_procedure_status,
            ow_repository=state_manager.ow_repository,
            ambtsgebied_ow_id=str(ambtsgebied_id),
        )
        regelinggebied_state = regelinggebied_builder.create_regelingsgebieden()

        # todo fill using repo or skip if not needed
        locaties_file = {
            "filename": "owLocaties.xml",
            "leveringsId": leveringid,
            "objectTypen": [],
            "gebiedengroepen": [],
            "gebieden": [],
            "ambtsgebieden": [],
        }
        divisies_files = {
            "filename": "owDivisie.xml",
            "leveringsId": leveringid,
            "objectTypen": [],
            "annotaties": [],
        }
        regelinggebied_file = {
            "filename": "owRegelingsgebied.xml",
            "leveringsId": leveringid,
            "objectTypen": [],
            "regelingsgebieden": [],
        }
        state_manager.created_ow_object_ids = state_manager.ow_repository.get_created_objects_id_list()
        state_manager.created_ow_objects_map = state_manager.ow_repository.get_ow_object_mapping()

        state_manager.ow_repository.store_locaties_content(locaties_state)
        state_manager.ow_repository.store_divisie_content(divisie_state)
        state_manager.ow_repository.store_regelingsgebied_content(regelinggebied_state)

        ow_manifest_builder = ManifestBuilder(
            act_work=str(state_manager.input_data.publication_settings.regeling_frbr.get_work()),
            doel=state_manager.input_data.publication_settings.instelling_doel.frbr,
        )
        manifest_file = ow_manifest_builder.create_manifest(
            state_manager.ow_repository.divisie_content,
            state_manager.ow_repository.locaties_content,
            state_manager.ow_repository.regelingsgebied_content,
        )

        state_manager.add_output_file(owlocaties)
        state_manager.add_output_file(owdivisies)
        state_manager.add_output_file(owregelinggebied)
        state_manager.add_output_file(ow_manifest_file)

        return state_manager
