from typing import Optional, List

from ....models import ContentType
from ....services.ow.enums import IMOWTYPES, OwProcedureStatus, OwRegelingsgebiedObjectType
from ....services.ow.models import OWRegelingsgebied, OWLocatie, OWObject
from ....services.ow.ow_id import generate_ow_id
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.states.ow_repository import OWRepository
from ...state_manager.exceptions import OWStateError
from .ow_file_builder import OwTemplateData, OwFileBuilder


class OwRegelingsgebiedFileData(OwTemplateData):
    object_typen: List[OwRegelingsgebiedObjectType]
    ow_objecten: List[OWObject]


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
        ow_repository: OWRepository,
        ambtsgebied_ow_id: str,
        ow_procedure_status: Optional[OwProcedureStatus],
    ):
        super().__init__()
        self._provincie_id = provincie_id
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._ambtsgebied = ambtsgebied_ow_id

    def handle_ow_object_changes(self) -> None:
        # if provided with existing ambtsgebied, mutation required.
        known_ambtsgebied_id = self._ow_repository.get_existing_ambtsgebied_id(self._ambtsgebied_data.UUID)
        if known_ambtsgebied_id:
            known_regelingsgebied_id = self._ow_repository.get_existing_regelingsgebied_id(known_ambtsgebied_id)
            if not known_regelingsgebied_id:
                raise OWStateError("Ambtsgebied known, but no regelingsgebied found in state.")
            self._mutate_regelingsgebied(
                known_regelingsgebied_id=known_regelingsgebied_id, new_ambtsgebied_id=known_ambtsgebied_id
            )
        else:
            # or assume inital version and create new regelingsgebied.
            self._create_regelingsgebied()

    def _create_regelingsgebied(self):
        ow_id: str = generate_ow_id(IMOWTYPES.REGELINGSGEBIED, self._provincie_id)
        regelingsgebied = OWRegelingsgebied(
            OW_ID=ow_id,
            ambtsgebied=self._ambtsgebied,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(regelingsgebied)
        return regelingsgebied

    def _mutate_regelingsgebied(self, known_regelingsgebied_id: str, new_ambtsgebied_id: str):
        regelingsgebied = OWRegelingsgebied(
            OW_ID=known_regelingsgebied_id,
            ambtsgebied=new_ambtsgebied_id,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_mutated_ow(regelingsgebied)
        return regelingsgebied

    def create_file(self, levering_id: str, ow_objects: List[OWLocatie]) -> OutputFile:
        file_data = OwRegelingsgebiedFileData(
            filename=self.file_name,
            levering_id=levering_id,
            object_typen=self.get_used_ow_object_types(ow_objects),
            ow_objecten=ow_objects,
            ow_procedure_status=self._ow_procedure_status,
        )
        content = load_template(
            template_name=self.template_path,
            pretty_print=True,
            data=file_data,
        )
        output_file = OutputFile(
            filename=self.file_name,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
