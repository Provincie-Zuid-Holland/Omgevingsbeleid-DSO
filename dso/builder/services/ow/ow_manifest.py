from ....models import ContentType, DoelFRBR
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class ManifestContent:
    def __init__(self, act_akn: str, doel: DoelFRBR):
        self._act_akn = act_akn
        self._doel = doel

    def create_manifest(self, divisie_data, locaties_data, regelingsgebied_data) -> OutputFile:
        file_data = []
        file_data.append({"naam": divisie_data["filename"], "objecttypes": divisie_data["objectTypen"]})
        file_data.append({"naam": regelingsgebied_data["filename"], "objecttypes": regelingsgebied_data["objectTypen"]})
        file_data.append({"naam": locaties_data["filename"], "objecttypes": locaties_data["objectTypen"]})

        output_file: OutputFile = self._create_manifest_file(file_data)
        return output_file

    def _create_manifest_file(self, file_data) -> OutputFile:
        content = load_template(
            "ow/manifest-ow.xml",
            pretty_print=True,
            act_akn=self._act_akn,
            doel_id=self._doel.get_work(),
            files=file_data,
        )
        output_file = OutputFile(
            filename="manifest-ow.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
