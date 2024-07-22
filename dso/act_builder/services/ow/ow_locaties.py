from typing import List, Optional, Set

from pydantic.main import BaseModel

from ....services.ow.enums import IMOWTYPES, OwLocatieObjectType, OwProcedureStatus
from ....services.ow.models import BestuurlijkeGrenzenVerwijzing, OWAmbtsgebied, OWGebied, OWGebiedenGroep, OWObject
from ....services.ow.ow_id import generate_ow_id
from ...state_manager.input_data.ambtsgebied import Ambtsgebied
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Locatie, Werkingsgebied
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_file_builder import OwFileBuilder


class OwLocatieTemplateData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[OwLocatieObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []

    @property
    def object_type_list(self) -> List[str]:
        return [obj.value for obj in self.object_types]


class OwLocatieBuilder(OwFileBuilder):
    FILE_NAME = "owLocaties.xml"
    TEMPLATE_PATH = "ow/owLocaties.xml"

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ambtsgebied: Ambtsgebied,
        werkingsgebieden: List[Werkingsgebied],
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        super().__init__()
        self._provincie_id: str = provincie_id
        self._levering_id: str = levering_id
        self._werkingsgebieden = werkingsgebieden
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._ambtsgebied_data = ambtsgebied
        self._used_object_types: Set[OwLocatieObjectType] = set()

    def handle_ow_object_changes(self) -> None:
        """
        Compares werkingsgebied objects with previous OW state and
        determines if new, mutation or termination action is needed.
        """
        existing_ambtsgebied = self._ow_repository.get_existing_ambtsgebied_id(self._ambtsgebied_data.UUID)
        if not existing_ambtsgebied:
            self.create_ow_ambtsgebied(self._ambtsgebied_data)
            # TODO: Add termination of previous ambtsgebied
            # Requires storing full aoj data to ow state

        for werkingsgebied in self._werkingsgebieden:
            existing_ow_gebied: Optional[OWGebied] = self._ow_repository.get_known_gebied_by_code(
                werkingsgebied_code=werkingsgebied.Code
            )
            if not existing_ow_gebied:
                self.new_ow_gebiedengroep(werkingsgebied)
            else:
                if existing_ow_gebied.mapped_uuid != werkingsgebied.UUID:
                    # if existing werkingsgebied code in state, with a new external UUID, mutate
                    self.mutate_ow_gebied(
                        locatie=werkingsgebied.Locaties[0],
                        existing_gebied_id=existing_ow_gebied.OW_ID,
                        code=werkingsgebied.Code,
                    )

                # gebiedengroep mutation not yet needed
                # self.mutate_ow_gebiedengroep(werkingsgebied, existing_gebiedengroep_id)

    def new_ow_gebied(self, locatie: Locatie, werkingsgebied_code: str) -> OWGebied:
        new_ow_id = generate_ow_id(IMOWTYPES.GEBIED, self._provincie_id)
        gebied = OWGebied(
            OW_ID=new_ow_id,
            mapped_uuid=locatie.UUID,
            noemer=locatie.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied_code,
        )
        self._ow_repository.add_new_ow(gebied)
        return gebied

    def new_ow_gebiedengroep(self, werkingsgebied: Werkingsgebied) -> OWGebiedenGroep:
        gebieden: List[str] = []
        for locatie in werkingsgebied.Locaties:
            new_gebied = self.new_ow_gebied(locatie, werkingsgebied.Code)
            gebieden.append(new_gebied.OW_ID)

        new_group_ow_id = generate_ow_id(IMOWTYPES.GEBIEDENGROEP, self._provincie_id)
        new_gebiedengroep = OWGebiedenGroep(
            OW_ID=new_group_ow_id,
            mapped_uuid=werkingsgebied.UUID,
            noemer=werkingsgebied.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied.Code,
            gebieden=gebieden,
        )
        self._ow_repository.add_new_ow(new_gebiedengroep)
        return new_gebiedengroep

    def mutate_ow_gebied(self, locatie: Locatie, existing_gebied_id: str, code: str) -> OWGebied:
        # ow obj mutation means deliver OW object with new data but same OW_ID
        mutated_obj = OWGebied(
            OW_ID=existing_gebied_id,
            mapped_uuid=locatie.UUID,
            noemer=locatie.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=code,
        )
        self._ow_repository.add_mutated_ow(mutated_obj)
        return mutated_obj

    def mutate_ow_gebiedengroep(
        self, werkingsgebied: Werkingsgebied, existing_gebiedengroep_id: str
    ) -> OWGebiedenGroep:
        # ow obj mutation means deliver OW object with new data but same OW_ID
        mutated_gebiedengroep = OWGebiedenGroep(
            OW_ID=existing_gebiedengroep_id,
            mapped_uuid=werkingsgebied.UUID,
            noemer=werkingsgebied.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied.Code,
        )
        for locatie in werkingsgebied.Locaties:
            existing_gebied = self._ow_repository.get_known_gebied_by_code(werkingsgebied.Code)
            if not existing_gebied:
                # Gebiedengroep and Gebied currently 1-1 matched
                # Not supported to mutate a existing gebiedengroep with non existing gebied
                raise NotImplementedError("Expected existing owgebied in state to apply to mutated gebiedengroep")

            mutated_gebied = self.mutate_ow_gebied(locatie, existing_gebied.OW_ID, werkingsgebied.Code)
            mutated_gebiedengroep.gebieden.append(mutated_gebied.OW_ID)

        self._ow_repository.add_mutated_ow(mutated_gebiedengroep)
        return mutated_gebiedengroep

    def create_ow_ambtsgebied(self, ambtsgebied_data: Ambtsgebied) -> OWAmbtsgebied:
        gebied_ow_id = generate_ow_id(IMOWTYPES.AMBTSGEBIED, self._provincie_id)
        new_ambtsgebied: OWAmbtsgebied = OWAmbtsgebied(
            OW_ID=gebied_ow_id,
            bestuurlijke_grenzen_verwijzing=BestuurlijkeGrenzenVerwijzing(
                bestuurlijke_grenzen_id=self._provincie_id.upper(),
                domein=ambtsgebied_data.domein,
                geldig_op=ambtsgebied_data.geldig_op,
            ),
            mapped_uuid=ambtsgebied_data.UUID,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(new_ambtsgebied)
        return new_ambtsgebied

    def get_used_object_types(self) -> List[OwLocatieObjectType]:
        return list(self._used_object_types)

    def add_used_ow_object_types(self, ow_objects: List[OWObject]) -> None:
        for obj in ow_objects:
            if isinstance(obj, OWGebied):
                self._used_object_types.add(OwLocatieObjectType.GEBIED)
            elif isinstance(obj, OWGebiedenGroep):
                self._used_object_types.add(OwLocatieObjectType.GEBIEDENGROEP)
            elif isinstance(obj, OWAmbtsgebied):
                self._used_object_types.add(OwLocatieObjectType.AMBTSGEBIED)

    def build_template_data(self) -> Optional[OwLocatieTemplateData]:
        new_locations = self._ow_repository.get_new_locations()
        mutated_locations = self._ow_repository.get_mutated_locations()
        terminated_locations = self._ow_repository.get_terminated_locations()

        if not (new_locations or mutated_locations or terminated_locations):
            return None

        # find all used object types in this file
        self.add_used_ow_object_types(new_locations + mutated_locations + terminated_locations)

        template_data = OwLocatieTemplateData(
            levering_id=self._levering_id,
            object_types=self.get_used_object_types(),
            new_ow_objects=new_locations,
            mutated_ow_objects=mutated_locations,
            terminated_ow_objects=terminated_locations,
            procedure_status=self._ow_procedure_status,
        )
        self.template_data = template_data
        return template_data
