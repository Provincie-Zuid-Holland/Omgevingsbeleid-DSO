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
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_file_builder import OwFileBuilder


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
    Assuming that regelinggebied and ambstgebied should only be
    delivered on initial version of an act, then updated together.

    based on TPOD 3.0:
    https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20231215/#0F625002
    """

    FILE_NAME = "owRegelingsgebied.xml"
    TEMPLATE_PATH = "ow/owRegelingsgebied.xml"

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ):
        super().__init__()
        self._provincie_id = provincie_id
        self._levering_id = levering_id
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._used_object_types = [OwRegelingsgebiedObjectType.REGELINGSGEBIED]
        self._ambtsgebied: Optional[OWAmbtsgebied] = None

    def get_ambtsgebied(self) -> Optional[OWAmbtsgebied]:
        return self._ambtsgebied

    def get_used_object_types(self) -> List[str]:
        return [obj.value for obj in self._used_object_types]

    def handle_ow_object_changes(self) -> None:
        """
        Either create a new regelingsgebied for a new ambtsgebied given or
        if existing ambtsgebied was mutated, mutate the matching regelingsgebied reference.
        """
        self._ambtsgebied = self._ow_repository.get_ambtsgebied()
        if not self._ambtsgebied:
            # no changes to regelingsgebied needed so exit
            return

        known_ambtsgebied_id = self._ow_repository.get_existing_ambtsgebied_id(self._ambtsgebied.mapped_uuid)
        if not known_ambtsgebied_id:
            # new ambtsgebied so new regelingsgebied
            self._create_regelingsgebied()
        else:
            # existing ambtsgebied so mutating regelingsgebied
            known_regelingsgebied_id = self._ow_repository.get_existing_regelingsgebied_id(known_ambtsgebied_id)
            if not known_regelingsgebied_id:
                raise OWStateError("Ambtsgebied known, but no regelingsgebied found in state.")
            self._mutate_regelingsgebied(
                known_regelingsgebied_id=known_regelingsgebied_id, new_ambtsgebied_id=known_ambtsgebied_id
            )

    def _create_regelingsgebied(self) -> OWRegelingsgebied:
        if not self._ambtsgebied:
            raise OWStateError("Ambtsgebied is required to create a new regelingsgebied.")

        ow_id: str = generate_ow_id(IMOWTYPES.REGELINGSGEBIED, self._provincie_id)
        regelingsgebied = OWRegelingsgebied(
            OW_ID=ow_id,
            ambtsgebied=self._ambtsgebied.OW_ID,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(regelingsgebied)
        return regelingsgebied

    def _mutate_regelingsgebied(self, known_regelingsgebied_id: str, new_ambtsgebied_id: str) -> OWRegelingsgebied:
        regelingsgebied = OWRegelingsgebied(
            OW_ID=known_regelingsgebied_id,
            ambtsgebied=new_ambtsgebied_id,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_mutated_ow(regelingsgebied)
        return regelingsgebied

    def build_template_data(self) -> OwRegelingsgebiedFileData:
        new_regelingsgebieden = self._ow_repository.get_new_regelingsgebied()
        mutated_regelingsgebieden = self._ow_repository.get_mutated_regelingsgebied()
        terminated_regelingsgebieden = self._ow_repository.get_terminated_regelingsgebied()

        template_data = OwRegelingsgebiedFileData(
            levering_id=self._levering_id,
            object_types=self._used_object_types,
            new_ow_objects=new_regelingsgebieden,
            mutated_ow_objects=mutated_regelingsgebieden,
            terminated_ow_objects=terminated_regelingsgebieden,
            procedure_status=self._ow_procedure_status,
        )
        self.template_data = template_data
        return template_data
