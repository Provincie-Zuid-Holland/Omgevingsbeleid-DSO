from ....models import ContentType
from ....services.ow.enums import IMOWTYPES, OwProcedureStatus, OwRegelingsgebiedObjectType
from ....services.ow.models import OWRegelingsgebied
from ....services.ow.ow_id import generate_ow_id
from ....services.utils.helpers import load_template
from ...state_manager.input_data.ambtsgebied import Ambtsgebied
from ...state_manager.models import OutputFile, StrContentData


class OwRegelingsgebiedContent:
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
        ow_procedure_status: OwProcedureStatus,
        ambtsgebied: Ambtsgebied,
    ):
        self.provincie_id: str = provincie_id
        self.levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self.ambtsgebied = ambtsgebied
        self.xml_data = {
            "filename": "owRegelingsgebied.xml",
            "leveringsId": self.levering_id,
            "objectTypen": [],
            "regelingsgebieden": [],
        }
        self.file = None

    def create_regelingsgebieden(self):
        regelingsgebied = self._create_regelingsgebied()
        self.xml_data["regelingsgebieden"].append(regelingsgebied)
        self.xml_data["objectTypen"].append(OwRegelingsgebiedObjectType.REGELINGSGEBIED.value)
        self.file = self.create_file()
        return self.xml_data

    def _create_regelingsgebied(self):
        """
        Always include regelingsgebied once for a bill+act.
        Point to existing ambtsgebied if available in state.
        """
        ow_id: str = generate_ow_id(
            IMOWTYPES.REGELINGSGEBIED,
            self.provincie_id,
            self.ambtsgebied.identificatie_suffix,
        )
        ambtsgebied_ow_id: str = generate_ow_id(
            IMOWTYPES.AMBTSGEBIED,
            self.provincie_id,
            self.ambtsgebied.identificatie_suffix,
        )
        regelingsgebied = OWRegelingsgebied(
            OW_ID=ow_id,
            ambtsgebied=ambtsgebied_ow_id,
        )
        regelingsgebied.procedure_status = self.ow_procedure_status
        return regelingsgebied

    def create_file(self):
        content = load_template(
            "ow/owRegelingsgebied.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owRegelingsgebied.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
