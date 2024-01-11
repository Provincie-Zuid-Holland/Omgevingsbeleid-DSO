from ....models import ContentType
from ....services.ow.enums import OwDivisieObjectType
from ....services.ow.exceptions import OWObjectGenerationError
from ....services.ow.models import Annotation, OWDivisie, OWDivisieTekst, OWTekstDeel
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class OwDivisieContent:
    """
    Prepares the content for the OWDivisies file from object_tekst_lookup.
    """

    def __init__(self, object_tekst_lookup, levering_id):
        self.object_tekst_lookup = object_tekst_lookup
        self.levering_id = levering_id
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
            ow_text_mapping = OWTekstDeel(divisie=None, locations=[values["ow_location_id"]])

            if values["tag"] == "Divisietekst":
                ow_div = OWDivisieTekst(wid=values["wid"])
                object_type = OwDivisieObjectType.DIVISIETEKST.value
                ow_text_mapping.divisie = ow_div.OW_ID
                annotations.append(Annotation(divisietekst_aanduiding=ow_div, tekstdeel=ow_text_mapping))
            elif values["tag"] == "Divisie":
                ow_div = OWDivisie(wid=values["wid"])
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
            "templates/ow/owDivisie.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owDivisie.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
