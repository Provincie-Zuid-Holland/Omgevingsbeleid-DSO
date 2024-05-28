from typing import List

from pydantic import BaseModel

from ....models import ActFRBR, DoelFRBR
from .ow_file_builder import OwFileBuilder


class OwManifestBestand(BaseModel):
    naam: str
    objecttypes: List[str]


class OwManifestTemplateData(BaseModel):
    act_work: str
    doel: str
    files: List[OwManifestBestand]


class OwManifestBuilder(OwFileBuilder):
    FILE_NAME = "manifest-ow.xml"
    TEMPLATE_PATH = "ow/manifest-ow.xml"

    def __init__(
        self,
        act: ActFRBR,
        doel: DoelFRBR,
        manifest: List[OwManifestBestand] = [],
    ):
        super().__init__()
        self._act = act
        self._doel = doel
        self._manifest = manifest

    def add_manifest_item(self, file_name: str, object_types: List[str]) -> None:
        manifest_entry = OwManifestBestand(naam=file_name, objecttypes=object_types)
        self._manifest.append(manifest_entry)

    def handle_ow_object_changes(self) -> None:
        # No changes made in manifest
        pass

    def build_template_data(self) -> OwManifestTemplateData:
        template_data = OwManifestTemplateData(
            act_work=self._act.get_work(), doel=self._doel.get_work(), files=self._manifest
        )
        self.template_data = template_data
        return template_data
