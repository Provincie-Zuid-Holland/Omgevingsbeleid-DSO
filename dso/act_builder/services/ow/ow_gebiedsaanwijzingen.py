from typing import List, Optional, Set

from pydantic.main import BaseModel

from ....services.ow.enums import IMOWTYPES, OwGebiedsaanwijzingObjectType, OwProcedureStatus
from ....services.ow.models import (
    OWGebied,
    OWGebiedenGroep,
    OWObject,
    OWGebiedsaanwijzing,
)
from ....services.ow.ow_id import generate_ow_id
from ...state_manager.input_data.ambtsgebied import Ambtsgebied
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Locatie, Werkingsgebied
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_file_builder import OwFileBuilder


class OwGebiedsaanwijzingTemplateData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[OwGebiedsaanwijzingObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []

    @property
    def object_type_list(self) -> List[str]:
        return [obj.value for obj in self.object_types]


class OwGebiedsaanwijzingBuilder(OwFileBuilder):
    FILE_NAME = "owGebiedsaanwijzingen.xml"
    TEMPLATE_PATH = "ow/owGebiedsaanwijzingen.xml"

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        super().__init__()
        self._provincie_id: str = provincie_id
        self._levering_id: str = levering_id
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._used_object_types: Set[OwGebiedsaanwijzingTemplateData] = set()

    def handle_ow_object_changes(self) -> None:
        """
        Handle all OW object changes in the state
        """
        # gebiedsaw1 = self.new_ow_gebiedsaanwijzing()
        pass

    def new_ow_gebiedsaanwijzing(self):
        new_ow_id = generate_ow_id(IMOWTYPES.GEBIEDSAANWIJZING, self._provincie_id)
        input_dict = {
            "OW_ID": new_ow_id,
            "naam": "testgebied",
            "type_": "Bodem",
            "groep": "Bodembeheergebied",
            "locaties": ["nl.imow-pv28.gebiedengroep.d171debcd2d947adb0beada8515c7495"],
        }
        gebiedawz = OWGebiedsaanwijzing(**input_dict)
        self._ow_repository.add_new_ow(gebiedawz)

        return gebiedawz

    def build_template_data(self):
        new = self._ow_repository.get_new_gebiedsaanwijzingen()
        mutated = self._ow_repository.get_mutated_gebiedsaanwijzingen()
        terminated = self._ow_repository.get_terminated_gebiedsaanwijzingen()

        if not (new or mutated or terminated):
            return None

        template_data = OwGebiedsaanwijzingTemplateData(
            levering_id=self._levering_id,
            procedure_status=self._ow_procedure_status,
            object_types=[OwGebiedsaanwijzingObjectType.Gebiedsaanwijzing],
            new_ow_objects=new,
            mutated_ow_objects=mutated,
            terminated_ow_objects=terminated,
        )
        return template_data
