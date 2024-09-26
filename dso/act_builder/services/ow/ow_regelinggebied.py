from typing import List, Optional

from pydantic.main import BaseModel

from ....services.ow import (
    IMOWTYPES,
    OWAmbtsgebied,
    OWObject,
    OwProcedureStatus,
    OWRegelingsgebied,
    OwRegelingsgebiedObjectType,
    generate_ow_id,
)
from ...state_manager.exceptions import OWStateError
from .ow_file_builder import OwFileBuilder
from .ow_builder_context import BuilderContext
from ...state_manager.states.ow_repository import OWStateRepository


class OwRegelingsgebiedFileData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[OwRegelingsgebiedObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []

    @property
    def object_type_list(self) -> List[str]:
        return [obj.value for obj in self.object_types]


class OwRegelingsgebiedBuilder(OwFileBuilder):
    """
    Prepares the content for the OWRegelingGebied.
    Assuming that regelinggebied and ambtsgebied should only be
    delivered on initial version of an act, then updated together.

    based on TPOD 3.0:
    https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20231215/#0F625002
    """

    FILE_NAME = "owRegelingsgebied.xml"
    TEMPLATE_PATH = "ow/owRegelingsgebied.xml"

    def __init__(self, context: BuilderContext, ow_repository: OWStateRepository):
        super().__init__()
        self._context = context
        self._used_object_types = [OwRegelingsgebiedObjectType.REGELINGSGEBIED]
        self._ambtsgebied: Optional[OWAmbtsgebied] = None
        self._ow_repository = ow_repository

    def get_ambtsgebied(self) -> Optional[OWAmbtsgebied]:
        return self._ambtsgebied

    def get_used_object_types(self) -> List[str]:
        return [obj.value for obj in self._used_object_types]

    def handle_ow_object_changes(self) -> None:
        new_ambtsgebied = self._ow_repository.get_new_ambtsgebied()

        if not new_ambtsgebied:
            # No ambtsgebied ref changes, so exit early
            return

        self._ambtsgebied = new_ambtsgebied

        # Check for existing regelingsgebied
        known_regelingsgebied = self._ow_repository.get_existing_regelingsgebied()

        if known_regelingsgebied:
            # Mutate reference if existing regelingsgebied found
            self._mutate_regelingsgebied(
                existing_regelingsgebied=known_regelingsgebied, new_ambtsgebied_ref=self._ambtsgebied.OW_ID
            )
            return

        # If no existing regelingsgebied, ensure ambtsgebied exists before creation
        if not self._ambtsgebied:
            raise OWStateError("Ambtsgebied required to create new regelingsgebied.")

        # Create initial regelingsgebied
        self._create_regelingsgebied(ambtsgebied_ref=self._ambtsgebied.OW_ID)

    def _create_regelingsgebied(self, ambtsgebied_ref: str) -> OWRegelingsgebied:
        ow_id: str = generate_ow_id(IMOWTYPES.REGELINGSGEBIED, self._context.provincie_id)
        regelingsgebied = OWRegelingsgebied(
            OW_ID=ow_id,
            ambtsgebied=ambtsgebied_ref,
            procedure_status=self._context.ow_procedure_status,
        )
        self._ow_repository.add_new_ow(regelingsgebied)
        return regelingsgebied

    def _mutate_regelingsgebied(
        self, existing_regelingsgebied: OWRegelingsgebied, new_ambtsgebied_ref: str
    ) -> OWRegelingsgebied:
        updated_regelingsgebied = existing_regelingsgebied.copy(deep=True)
        updated_regelingsgebied.ambtsgebied = new_ambtsgebied_ref
        self._ow_repository.add_mutated_ow(updated_regelingsgebied)
        return updated_regelingsgebied

    def build_template_data(self) -> OwRegelingsgebiedFileData:
        new_regelingsgebieden = self._ow_repository.get_new_regelingsgebied()
        mutated_regelingsgebieden = self._ow_repository.get_mutated_regelingsgebied()
        terminated_regelingsgebieden = self._ow_repository.get_terminated_regelingsgebied()

        template_data = OwRegelingsgebiedFileData(
            levering_id=self._context.levering_id,
            object_types=self._used_object_types,
            new_ow_objects=new_regelingsgebieden,
            mutated_ow_objects=mutated_regelingsgebieden,
            terminated_ow_objects=terminated_regelingsgebieden,
            procedure_status=self._context.ow_procedure_status,
        )
        self.template_data = template_data
        return template_data
