from ....models import ContentType
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class ManifestContent:
    """
    Prepares the content for the Manifest OW file
    """

    def __init__(self, act_akn, doel):
        self.act_akn = act_akn
        self.doel = doel
        self.xml_data = {
            "act_akn": self.act_akn,
            "doel_id": f"/join/id/proces/pv28/{self.doel.jaar}/{self.doel.naam}",
        }
        self.file = None

    def create_manifest(self, divisie_data, locaties_data, regelingsgebied_data):
        file_data = []
        file_data.append({"naam": divisie_data["filename"], "objecttypes": divisie_data["objectTypen"]})
        file_data.append({"naam": regelingsgebied_data["filename"], "objecttypes": regelingsgebied_data["objectTypen"]})
        file_data.append({"naam": locaties_data["filename"], "objecttypes": locaties_data["objectTypen"]})
        self.xml_data["files"] = file_data
        self.file = self._create_manifest_file()

    def _create_manifest_file(self):
        content = load_template(
            "ow/manifest-ow.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="manifest-ow.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
