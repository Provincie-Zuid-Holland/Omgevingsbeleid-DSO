from ....models import ContentType
from ....services.ow.enums import OwDivisieObjectType, OwProcedureStatus
from ....services.ow.exceptions import OWObjectGenerationError
from ....services.ow.models import Annotation, OWDivisie, OWDivisieTekst, OWTekstDeel
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class OwDivisieContent:
    """
    Prepares the content for the OWDivisies file from object_tekst_lookup.
    """

    def __init__(
        self,
        object_tekst_lookup: dict,
        levering_id: str,
        ow_procedure_status: OwProcedureStatus,
    ):
        self.object_tekst_lookup = object_tekst_lookup
        self.levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self.xml_data = {
            "filename": "owDivisie.xml",
            "leveringsId": self.levering_id,
            "objectTypen": [],
            "annotaties": [],
        }
        self.file = None

    def create_divisies(self):
        """
        Create OWDivisie and OWTekstDeel objects and return them as output file
        """
        self._create_ow_divisies()
        self.file = self.create_file()
        return self.xml_data

    def _create_ow_divisies(self):
        """
        Create new OW Divisie annotations from locaties and
        policy objects using object_tekst_lookup.
        """
        object_types = self.xml_data["objectTypen"]
        annotations = self.xml_data["annotaties"]

        for object_code, values in self.object_tekst_lookup.items():
            if not values["gebied_uuid"]:
                continue

            ow_div = None
            ow_text_mapping = OWTekstDeel(
                divisie=None,
                locations=[values["ow_location_id"]],
                procedure_status=self.ow_procedure_status,
            )

            if values["tag"] == "Divisietekst":
                ow_div = OWDivisieTekst(wid=values["wid"], procedure_status=self.ow_procedure_status)
                object_type = OwDivisieObjectType.DIVISIETEKST.value
                ow_text_mapping.divisie = ow_div.OW_ID
                annotations.append(Annotation(divisietekst_aanduiding=ow_div, tekstdeel=ow_text_mapping))
            elif values["tag"] == "Divisie":
                ow_div = OWDivisie(wid=values["wid"], procedure_status=self.ow_procedure_status)
                object_type = OwDivisieObjectType.DIVISIE.value
                ow_text_mapping.divisie = ow_div.OW_ID
                annotations.append(Annotation(divisie_aanduiding=ow_div, tekstdeel=ow_text_mapping))
            else:
                raise OWObjectGenerationError("Expected annotation text tag to be either Divisie or Divisietekst.")

            if object_type not in object_types:
                object_types.append(object_type)

        if OwDivisieObjectType.TEKSTDEEL.value not in object_types:
            object_types.append(OwDivisieObjectType.TEKSTDEEL.value)

    def create_file(self):
        content = load_template(
            "ow/owDivisie.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owDivisie.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
