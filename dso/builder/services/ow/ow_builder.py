from typing import Optional

from ....services.ow.enums import OwProcedureStatus
from ....services.utils.waardelijsten import ProcedureType
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieContent
from ...services.ow.ow_locaties import OwLocatiesContent
from ...services.ow.ow_manifest import ManifestContent
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedContent
from ...state_manager.input_data.ambtsgebied import Ambtsgebied
from ...state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    """
    The OwBuilder class is responsible for building IMOW related objects
    and generating output files in XML format.

    Builds: OWGebied, OWGebiedenGroep, OWDivisie, OWDivisieTekst, OWTekstDeel for annotating policy.
    """

    def apply(self, state_manager: StateManager) -> StateManager:
        """
        Create all ow objects and save the output files to state
        """
        provincie_id: str = state_manager.input_data.publication_settings.provincie_id
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()
        leveringid = state_manager.input_data.publication_settings.opdracht.id_levering

        ow_procedure_status: Optional[OwProcedureStatus] = None
        if state_manager.input_data.besluit.soort_procedure == ProcedureType.Ontwerpbesluit:
            ow_procedure_status = OwProcedureStatus.ONTWERP.value

        ambtsgebied: Ambtsgebied = state_manager.input_data.ambtsgebied

        locaties_content = OwLocatiesContent(
            provincie_id=provincie_id,
            werkingsgebieden=werkingsgebieden,
            object_tekst_lookup=state_manager.ewid_service.get_state_object_tekst_lookup(),
            levering_id=leveringid,
            ow_procedure_status=ow_procedure_status,
            ambtsgebied_data=ambtsgebied,
        )
        locaties_state = locaties_content.create_locations()
        state_manager.ow_repository.store_locaties_content(locaties_state)

        divisie_content = OwDivisieContent(
            object_tekst_lookup=state_manager.ewid_service.get_state_object_tekst_lookup(),
            levering_id=leveringid,
            ow_procedure_status=ow_procedure_status,
        )
        divisie_state = divisie_content.create_divisies()
        state_manager.ow_repository.store_divisie_content(divisie_state)

        # TODO: for new version publications ensure if no new ambtsgebied created, same regelingsgebied is used
        regelinggebied_content = OwRegelingsgebiedContent(
            provincie_id=provincie_id,
            levering_id=leveringid,
            ow_procedure_status=ow_procedure_status,
            ambtsgebied_ow_id=locaties_state["ambtsgebieden"][0].OW_ID,
        )
        regelinggebied_state = regelinggebied_content.create_regelingsgebieden()
        state_manager.ow_repository.store_regelingsgebied_content(regelinggebied_state)

        state_manager.ow_repository.get_created_objects()
        state_manager.created_ow_object_ids = state_manager.ow_repository.get_created_objects_id_list()
        state_manager.created_ow_objects_map = state_manager.ow_repository.get_ow_object_mapping()

        manifest_content = ManifestContent(
            act_work=str(state_manager.input_data.publication_settings.regeling_frbr.get_work()),
            doel=state_manager.input_data.publication_settings.doel,
        )
        manifest_file = manifest_content.create_manifest(
            state_manager.ow_repository.divisie_content,
            state_manager.ow_repository.locaties_content,
            state_manager.ow_repository.regelingsgebied_content,
        )

        state_manager.add_output_file(locaties_content.file)
        state_manager.add_output_file(divisie_content.file)
        state_manager.add_output_file(regelinggebied_content.file)
        state_manager.add_output_file(manifest_file)

        return state_manager
