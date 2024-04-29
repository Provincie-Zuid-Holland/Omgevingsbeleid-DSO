from typing import List, Optional

from ....models import ContentType
from ....services.ow.enums import IMOWTYPES, OwProcedureStatus
from ....services.ow.models import BestuurlijkeGrenzenVerwijzing, OWAmbtsgebied, OWGebied, OWGebiedenGroep
from ....services.ow.ow_id import generate_ow_id
from ....services.utils.helpers import load_template
from ...state_manager.input_data.ambtsgebied import Ambtsgebied
from ...state_manager.input_data.resource.werkingsgebied.werkingsgebied import Locatie, Werkingsgebied
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.states.ow_repository import OWStateRepository


class OwLocatieBuilder:
    def __init__(
        self,
        provincie_id: str,
        ambtsgebied: Ambtsgebied,
        werkingsgebieden: List[Werkingsgebied],
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        self._provincie_id: str = provincie_id
        self._werkingsgebieden = werkingsgebieden
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._ambtsgebied_data = ambtsgebied

    def new_ow_gebied(self, locatie: Locatie, werkingsgebied_code: str) -> OWGebied:
        new_ow_id = generate_ow_id(IMOWTYPES.GEBIED, self._provincie_id)
        gebied = OWGebied(
            OW_ID=new_ow_id,
            geo_uuid=locatie.UUID,
            noemer=locatie.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied_code,
        )
        self._ow_repository.add_new_ow(gebied)
        return gebied

    def new_ow_gebiedengroep(self, werkingsgebied: Werkingsgebied) -> OWGebiedenGroep:
        gebieden = []
        for locatie in werkingsgebied.Locaties:
            gebieden.append(self.new_ow_gebied(locatie, werkingsgebied.Code))

        new_group_ow_id = generate_ow_id(IMOWTYPES.GEBIEDENGROEP, self._provincie_id)
        new_gebiedengroep = OWGebiedenGroep(
            OW_ID=new_group_ow_id,
            geo_uuid=werkingsgebied.UUID,
            noemer=werkingsgebied.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied.Code,
            locations=gebieden,
        )
        self._ow_repository.add_new_ow(new_gebiedengroep)
        return new_gebiedengroep

    def mutate_ow_gebied(self, locatie: Locatie, existing_gebied_id: str, code: str) -> OWGebied:
        # ow obj mutation means deliver OW object with new data but same OW_ID
        mutated_obj = OWGebied(
            OW_ID=existing_gebied_id,
            geo_uuid=locatie.UUID,
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
            geo_uuid=werkingsgebied.UUID,
            noemer=werkingsgebied.Title,
            procedure_status=self._ow_procedure_status,
            mapped_geo_code=werkingsgebied.Code,
        )
        for locatie in werkingsgebied.Locaties:
            existing_gebied_owid = self._ow_repository.get_existing_gebied_id(werkingsgebied.Code)
            if not existing_gebied_owid:
                # Scenario where group is updated seperatly from locations, should not occur yet
                # as support multiple locations are not supported for now
                # new_gebied = self.new_ow_gebied(locatie, werkingsgebied.Code)
                # mutated_gebiedengroep.locations.append(new_gebied)
                raise NotImplementedError("Multiple locations in group not supported yet.")

            mutated_gebied = self.mutate_ow_gebied(locatie, existing_gebied_owid, werkingsgebied.Code)
            mutated_gebiedengroep.locations.append(mutated_gebied)

        self._ow_repository.add_mutated_ow(mutated_gebiedengroep)
        return mutated_gebiedengroep

    def handle_ow_object_changes(self) -> None:
        """
        Compares werkingsgebied objects with previous OW state and
        determines if new, mutation or termination action is needed.

        Create: werkingsgebied code that was not in previous ow state
        Mutation: existing werkingsgebied values MUST be different from existing OW obj
            or LVBB will not accept.
        Terminate: Only if specifically added in input_data, other terminations calc later
        """
        existing_ambtsgebied = self._ow_repository.get_existing_ambtsgebied_id(self._ambtsgebied_data.UUID)
        if not existing_ambtsgebied:
            self.create_ow_ambtsgebied(self._ambtsgebied_data)

        for werkingsgebied in self._werkingsgebieden:
            existing_gebied_id = self._ow_repository.get_existing_gebied_id(werkingsgebied.Code)
            if not existing_gebied_id:
                self.new_ow_gebiedengroep(werkingsgebied)
            else:
                self.mutate_ow_gebied(werkingsgebied.Locaties[0], existing_gebied_id, werkingsgebied.Code)
                # since we dont support adding new locations to existing groups yet, we only need to
                # mutate the owgebied as the group still references the same gebied ID>
                # self.mutate_ow_gebiedengroep(werkingsgebied, existing_gebiedengroep_id)

    def create_ow_ambtsgebied(self, ambtsgebied_data: Ambtsgebied) -> OWAmbtsgebied:
        gebied_ow_id = generate_ow_id(IMOWTYPES.AMBTSGEBIED, self._provincie_id)
        new_ambtsgebied: OWAmbtsgebied = OWAmbtsgebied(
            OW_ID=gebied_ow_id,
            bestuurlijke_genzenverwijzing=BestuurlijkeGrenzenVerwijzing(
                bestuurlijke_grenzen_id=self._provincie_id.upper(),
                domein=ambtsgebied_data.domein,
                geldig_op=ambtsgebied_data.geldig_op,
            ),
            mapped_uuid=ambtsgebied_data.UUID,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(new_ambtsgebied)
        return new_ambtsgebied

    def create_file(self, output_data: dict) -> OutputFile:
        content = load_template(
            "ow/owLocaties.xml",
            pretty_print=True,
            data=output_data,
        )
        output_file = OutputFile(
            filename="owLocaties.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
