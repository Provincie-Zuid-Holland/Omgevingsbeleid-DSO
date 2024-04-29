from typing import Optional

from ....models import ContentType
from ....services.ow.enums import IMOWTYPES, OwProcedureStatus, OwRegelingsgebiedObjectType
from ....services.ow.models import OWRegelingsgebied
from ....services.ow.ow_id import generate_ow_id
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.states.ow_repository import OWStateRepository


class OwRegelingsgebiedBuilder:
    """
    Prepares the content for the OWRegelingGebied
    Assuming that the regelinggebied is always part of a publication
    and that ambtsgebied should be upserted and shared between acts.
    based on TPOD 2.0.2
    https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20230407/#0F625002
    """

    def __init__(
        self,
        provincie_id: str,
        levering_id,
        ow_repository: OWStateRepository,
        ambtsgebied_ow_id: str,
        ow_procedure_status: Optional[OwProcedureStatus],
    ):
        self._provincie_id: str = provincie_id
        self._levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._ambtsgebied = ambtsgebied_ow_id
        self._xml_data = {
            "filename": "owRegelingsgebied.xml",
            "leveringsId": self._levering_id,
            "objectTypen": [],
            "regelingsgebieden": [],
        }
        self.file = None

    def create_regelingsgebieden(self):
        regelingsgebied = self._create_regelingsgebied()
        self._xml_data["regelingsgebieden"].append(regelingsgebied)
        self._xml_data["objectTypen"].append(OwRegelingsgebiedObjectType.REGELINGSGEBIED.value)
        self.file = self.create_file()
        return self._xml_data

    def _create_regelingsgebied(self):
        """
        Always include regelingsgebied once for a bill+act.
        Point to existing ambtsgebied if available in state.
        """
        # TODO: currently generates new OW ID every time. Read from input data if unchanged
        ow_id: str = generate_ow_id(IMOWTYPES.REGELINGSGEBIED, self._provincie_id)
        regelingsgebied = OWRegelingsgebied(
            OW_ID=ow_id,
            ambtsgebied=self._ambtsgebied,
            procedure_status=self.ow_procedure_status,
        )
        return regelingsgebied

    def create_file(self):
        content = load_template(
            "ow/owRegelingsgebied.xml",
            pretty_print=True,
            data=self._xml_data,
        )
        output_file = OutputFile(
            filename="owRegelingsgebied.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
