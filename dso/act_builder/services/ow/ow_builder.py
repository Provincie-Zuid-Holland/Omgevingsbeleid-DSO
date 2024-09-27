
from ....services.ow.ow_state_patcher import OWStatePatcher
from ...services import BuilderService
from ...services.ow.ow_divisie import OwDivisieBuilder
from ...services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from ...services.ow.ow_locaties import OwLocatieBuilder
from ...services.ow.ow_manifest import OwManifestBuilder
from ...services.ow.ow_regelinggebied import OwRegelingsgebiedBuilder
from ...state_manager.state_manager import StateManager


class OwBuilder(BuilderService):
    def __init__(
        self,
        locatie_builder: OwLocatieBuilder,
        divisie_builder: OwDivisieBuilder,
        gb_aanwijzing_builder: OwGebiedsaanwijzingBuilder,
        regelinggebied_builder: OwRegelingsgebiedBuilder,
        ow_manifest_builder: OwManifestBuilder,
        ow_state_patcher: OWStatePatcher,
    ):
        self._locatie_builder = locatie_builder
        self._divisie_builder = divisie_builder
        self._gb_aanwijzing_builder = gb_aanwijzing_builder
        self._regelinggebied_builder = regelinggebied_builder
        self._ow_manifest_builder = ow_manifest_builder
        self._ow_state_patcher = ow_state_patcher

    def apply(self, state_manager: StateManager) -> StateManager:
        self._process_object_changes()
        patched_ow_data = self._ow_state_patcher.patch(input_state_ow_data=state_manager.input_data.ow_data)
        state_manager.ow_object_state = patched_ow_data
        self._build_output_files(state_manager)

        return state_manager

    def _process_object_changes(self) -> None:
        """Handles OW object changes using the builders for each file."""
        self._locatie_builder.handle_ow_object_changes()
        self._divisie_builder.handle_ow_object_changes()
        self._gb_aanwijzing_builder.handle_ow_object_changes()
        self._regelinggebied_builder.handle_ow_object_changes()

    def _build_output_files(self, state_manager: StateManager) -> None:
        """Handles building and adding output files using the injected builders."""
        # Collect template data from each builder
        locatie_template_data = self._locatie_builder.build_template_data()
        divisie_template_data = self._divisie_builder.build_template_data()
        gebiedsaanwijzing_template_data = self._gb_aanwijzing_builder.build_template_data()
        regelingsgebied_template_data = self._regelinggebied_builder.build_template_data()

        # Generate output files
        if locatie_template_data:
            ow_locatie_file = self._locatie_builder.create_file(locatie_template_data.dict())
            self._ow_manifest_builder.add_manifest_item(
                self._locatie_builder.FILE_NAME, locatie_template_data.object_type_list
            )
            state_manager.add_output_file(ow_locatie_file)

        if divisie_template_data:
            ow_divisie_file = self._divisie_builder.create_file(divisie_template_data.dict())
            self._ow_manifest_builder.add_manifest_item(
                self._divisie_builder.FILE_NAME, divisie_template_data.object_type_list
            )
            state_manager.add_output_file(ow_divisie_file)

        if gebiedsaanwijzing_template_data:
            ow_gb_aanwijzing_file = self._gb_aanwijzing_builder.create_file(gebiedsaanwijzing_template_data.dict())
            self._ow_manifest_builder.add_manifest_item(
                self._gb_aanwijzing_builder.FILE_NAME, gebiedsaanwijzing_template_data.object_type_list
            )
            state_manager.add_output_file(ow_gb_aanwijzing_file)

        if regelingsgebied_template_data:
            ow_regelingsgebied_file = self._regelinggebied_builder.create_file(regelingsgebied_template_data.dict())
            self._ow_manifest_builder.add_manifest_item(
                self._regelinggebied_builder.FILE_NAME, self._regelinggebied_builder.get_used_object_types()
            )
            state_manager.add_output_file(ow_regelingsgebied_file)

        # Create and add manifest file
        ow_manifest_template_data = self._ow_manifest_builder.build_template_data()
        ow_manifest_file = self._ow_manifest_builder.create_file(ow_manifest_template_data.dict())
        state_manager.add_output_file(ow_manifest_file)


# class OwBuilderFactory:
#     """
#     A factory class responsible for creating a fully configured OwBuilder instance.
#     Takes a BuilderContext and returns an OwBuilder instance with all required file builders injected.
#     """

#     @staticmethod
#     def create_ow_builder(
#         context: BuilderContext,
#         ow_repository: OWStateRepository,
#         state_werkingsgebieden: List[Werkingsgebied],
#         ambtsgebied: Ambtsgebied,
#         annotation_lookup_map: dict,
#         act: ActFRBR,
#         doel: DoelFRBR,
#     ) -> OwBuilder:
#         # Create individual file builders
#         locatie_builder = OwLocatieBuilder(
#             context=context,
#             werkingsgebieden=state_werkingsgebieden,
#             ambtsgebied=ambtsgebied,
#             ow_repository=ow_repository,
#         )

#         divisie_builder = OwDivisieBuilder(
#             context=context,
#             annotation_lookup_map=annotation_lookup_map,
#             ow_repository=ow_repository,
#         )

#         gb_aanwijzing_builder = OwGebiedsaanwijzingBuilder(
#             context=context,
#             annotation_lookup_map=annotation_lookup_map,
#             ow_repository=ow_repository,
#         )

#         regelinggebied_builder = OwRegelingsgebiedBuilder(
#             context=context,
#             ow_repository=ow_repository,
#         )

#         ow_manifest_builder = OwManifestBuilder(
#             act=act,
#             doel=doel,
#         )

#         return OwBuilder(
#             locatie_builder=locatie_builder,
#             divisie_builder=divisie_builder,
#             gb_aanwijzing_builder=gb_aanwijzing_builder,
#             regelinggebied_builder=regelinggebied_builder,
#             ow_manifest_builder=ow_manifest_builder,
#             ow_state_patcher_factory=OWStatePatcher(ow_repository=ow_repository),
#         )
