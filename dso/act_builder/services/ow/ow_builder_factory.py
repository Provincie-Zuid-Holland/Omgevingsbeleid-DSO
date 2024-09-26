from typing import List, Optional, Callable, Tuple

from ....models import ActFRBR, DoelFRBR
from ....services.ow.enums import OwProcedureStatus
from ....services.ow.ow_state_patcher import OWStatePatcher
from ....services.utils.waardelijsten import ProcedureType
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager
from .ow_builder_context import BuilderContext
from .ow_builder import OwBuilder


class OwBuilderFactory:
    """
    A factory class responsible for creating a fully configured OwBuilder instance.
    It creates the BuilderContext and returns an OwBuilder instance with all required file builders injected.
    """

    @staticmethod
    def create_ow_builder(
        state_manager: StateManager,  # Use StateManager instead of BuilderContext to generate context
        annotation_lookup_map: dict,
        regeling_frbr: ActFRBR,
        doel_frbr: DoelFRBR,
    ) -> OwBuilder:
        # Create BuilderContext inside the factory
        context = OwBuilderFactory._create_builder_context(state_manager)

        # Create individual file builders using the context
        locatie_builder = OwLocatieBuilder(
            context=context,
            werkingsgebieden=state_manager.input_data.resources.werkingsgebied_repository.all(),
            ambtsgebied=state_manager.input_data.ambtsgebied,
            ow_repository=state_manager.ow_repository,
        )

        divisie_builder = OwDivisieBuilder(
            context=context,
            annotation_lookup_map=annotation_lookup_map,
            ow_repository=state_manager.ow_repository,
        )

        gb_aanwijzing_builder = OwGebiedsaanwijzingBuilder(
            context=context,
            annotation_lookup_map=annotation_lookup_map,
            ow_repository=state_manager.ow_repository,
        )

        regelinggebied_builder = OwRegelingsgebiedBuilder(
            context=context,
            ow_repository=state_manager.ow_repository,
        )

        ow_manifest_builder = OwManifestBuilder(
            regeling_frbr=regeling_frbr,
            doel_frbr=doel_frbr,
        )

        ow_state_patcher = OWStatePatcher(ow_repository=state_manager.ow_repository)

        # Return fully configured OwBuilder instance
        return OwBuilder(
            locatie_builder=locatie_builder,
            divisie_builder=divisie_builder,
            gb_aanwijzing_builder=gb_aanwijzing_builder,
            regelinggebied_builder=regelinggebied_builder,
            ow_manifest_builder=ow_manifest_builder,
            ow_state_patcher=ow_state_patcher,
        )

    @staticmethod
    def _create_builder_context(state_manager: StateManager) -> BuilderContext:
        """
        This method creates the BuilderContext based on the StateManager data.
        """
        orphaned_wids, orphaned_object_codes = OwBuilderFactory._calc_orphaned_wids(
            known_wid_map=state_manager.input_data.get_known_wid_map(),
            current_wid_map=state_manager.act_ewid_service.get_state_used_wid_map(),
            known_ow_wids=state_manager.ow_repository.get_existing_wid_list(),
        )

        return BuilderContext(
            provincie_id=state_manager.input_data.publication_settings.provincie_id,
            levering_id=state_manager.input_data.publication_settings.opdracht.id_levering,
            ow_procedure_status=OwBuilderFactory._get_ow_procedure_status(
                state_manager.input_data.besluit.soort_procedure
            ),
            orphaned_wids=orphaned_wids,
        )

    @staticmethod
    def _calc_orphaned_wids(known_wid_map, current_wid_map, known_ow_wids: List[str]):
        """
        Helper function to calculate orphaned WIDs for the BuilderContext.
        """
        orphaned_wids = []
        orphaned_object_codes = []
        for obj_code, wid in known_wid_map.items():
            if obj_code not in current_wid_map and wid in known_ow_wids:
                orphaned_wids.append(wid)
                orphaned_object_codes.append(obj_code)

        return orphaned_wids, orphaned_object_codes

    @staticmethod
    def _get_ow_procedure_status(soort_procedure: ProcedureType) -> Optional[OwProcedureStatus]:
        """Helper to determine the OW procedure status."""
        match soort_procedure:
            case ProcedureType.Ontwerpbesluit:
                return OwProcedureStatus.ONTWERP
            case ProcedureType.Definitief_besluit:
                return None
            case _:
                return None
