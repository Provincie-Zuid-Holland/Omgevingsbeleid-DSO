from ....models import ContentType
from ....services.ow.enums import OwProcedureStatus, OwRegelingsgebiedObjectType
from ....services.ow.models import OWRegelingsgebied
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class OwRegelingsgebiedContent:
    """
    Prepares the content for the OWRegelingGebied
    """

    def __init__(self, levering_id, ow_procedure_status: OwProcedureStatus):
        self.levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self.xml_data = {
            "filename": "owRegelingsgebied.xml",
            "leveringsId": self.levering_id,
            "objectTypen": [],
            "regelingsgebieden": [],
        }
        self.file = None

    def create_regelingen(self):
        self._create_ow_regelingen()
        self.file = self.create_file()
        return self.xml_data

    def _create_ow_regelingen(self):
        """
        Uses manual regelingsgebied as ow object for now.
        """
        ambtsgebied = OWRegelingsgebied(
            OW_ID="nl.imow-pv28.regelingsgebied.002000000000000000009928",
            ambtsgebied="nl.imow-pv28.ambtsgebied.002000000000000000009928",
            procedure_status=self.ow_procedure_status,
        )
        self.xml_data["regelingsgebieden"].append(ambtsgebied)
        self.xml_data["objectTypen"].append(OwRegelingsgebiedObjectType.REGELINGSGEBIED.value)

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
