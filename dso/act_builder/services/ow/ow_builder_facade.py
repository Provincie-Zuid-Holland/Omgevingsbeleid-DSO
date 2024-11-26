from typing import Dict, List, Optional

from ....services.ow.enums import OwProcedureStatus
from ....services.ow.ow_annotation_service import OWAnnotationService
from ....services.ow.ow_state_patcher import OWStatePatcher
from ....services.utils.waardelijsten import ProcedureType
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from ...services.ow.ow_hoofdlijnen import OwHoofdlijnBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager
from .ow_builder import OwBuilder
from .ow_builder_context import BuilderContext


class OwBuilderFacade(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        # build ow annotation map from policy objects data
        annotation_service = OWAnnotationService(
            werkingsgebied_repository=state_manager.input_data.resources.werkingsgebied_repository,
            policy_object_repository=state_manager.input_data.resources.policy_object_repository,
            used_wid_map=state_manager.act_ewid_service.get_state_used_wid_map(),
        )
        annotation_map = annotation_service.build_annotation_map()

        ow_builder: OwBuilder = self._create_ow_builder(state_manager, annotation_map)
        return ow_builder.apply(state_manager)

    def _create_ow_builder(self, state_manager: StateManager, annotation_lookup_map: dict) -> OwBuilder:
        context = self._create_builder_context(state_manager)

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
            debug_enabled=state_manager.debug_enabled,
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

        hoofdlijn_builder = OwHoofdlijnBuilder(
            context=context,
            annotation_lookup_map=annotation_lookup_map,
            ow_repository=state_manager.ow_repository,
        )

        ow_manifest_builder = OwManifestBuilder(
            regeling_frbr=state_manager.input_data.publication_settings.regeling_frbr,
            doel_frbr=state_manager.input_data.publication_settings.instelling_doel.frbr,
        )

        ow_state_patcher = OWStatePatcher(ow_repository=state_manager.ow_repository)

        return OwBuilder(
            locatie_builder=locatie_builder,
            divisie_builder=divisie_builder,
            gb_aanwijzing_builder=gb_aanwijzing_builder,
            regelinggebied_builder=regelinggebied_builder,
            hoofdlijn_builder=hoofdlijn_builder,
            ow_manifest_builder=ow_manifest_builder,
            ow_state_patcher=ow_state_patcher,
        )

    def _create_builder_context(self, state_manager: StateManager) -> BuilderContext:
        orphaned_wids: List[str] = self._calc_orphaned_wids(state_manager)
        ow_procedure_status: Optional[OwProcedureStatus] = self._get_ow_procedure_status(
            state_manager.input_data.besluit.soort_procedure
        )

        return BuilderContext(
            provincie_id=state_manager.input_data.publication_settings.provincie_id,
            levering_id=state_manager.input_data.publication_settings.opdracht.id_levering,
            ow_procedure_status=ow_procedure_status,
            orphaned_wids=orphaned_wids,
            imow_value_list_version=None,
        )

    def _calc_orphaned_wids(self, state_manager: StateManager) -> List[str]:
        known_wid_map: Dict[str, str] = state_manager.input_data.get_known_wid_map()
        current_wid_map: Dict[str, str] = state_manager.act_ewid_service.get_state_used_wid_map()
        known_ow_wids: List[str] = state_manager.ow_repository.get_existing_wid_list()

        orphaned_wids: List[str] = []
        for obj_code, wid in known_wid_map.items():
            if obj_code not in current_wid_map and wid in known_ow_wids:
                orphaned_wids.append(wid)

        return orphaned_wids

    def _get_ow_procedure_status(self, soort_procedure: ProcedureType) -> Optional[OwProcedureStatus]:
        match soort_procedure:
            case ProcedureType.Ontwerpbesluit:
                return OwProcedureStatus.ONTWERP
            case ProcedureType.Definitief_besluit:
                return None
