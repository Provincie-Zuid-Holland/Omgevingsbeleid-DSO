from dso.act_builder.services.ow.input.ow_input_factory import OwInputFactory
from dso.act_builder.services.ow.state.ow_state_builder import OwStateBuilder
from dso.act_builder.services.ow.state.ow_state_merger import MergeResult, OwStateMerger
from dso.act_builder.services.ow.xml.xml_builder import XmlBuilder

from ...builder_service import BuilderService
from ...state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        state_builder: OwStateBuilder = OwStateBuilder(
            state_manager.input_data.publication_settings.provincie_id,
            state_manager.input_data.besluit.soort_procedure,
        )

        input_factory: OwInputFactory = OwInputFactory(state_manager)
        state_builder.add_ambtsgebied(input_factory.get_ambtsgebied())
        state_builder.add_regelingsgebied(input_factory.get_regelingsgebied())
        state_builder.add_gebiedsaanwijzingen(input_factory.get_gebiedsaanwijzingen())
        state_builder.add_policy_objects(input_factory.get_policy_objects())
        state_builder.add_werkingsgebieden(input_factory.get_werkingsgebieden())

        state_merger: OwStateMerger = OwStateMerger()
        merge_result: MergeResult = state_merger.apply_into(
            state_builder.get_state(),
            state_manager.input_data.ow_state,
        )

        xml_builder = XmlBuilder(state_manager)
        xml_builder.build_files(merge_result.changeset)

        state_manager.output_ow_state = merge_result.result_state

        return state_manager
