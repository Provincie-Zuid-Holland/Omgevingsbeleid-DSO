from typing import Any, List, Dict

from pydantic import BaseModel

from ....models import DoelFRBR
from .ow_file_builder import OwFileBuilder


class OwManifestBestand(BaseModel):
    naam: str
    objecttypes: List[str]


class OwManifestTemplateData(BaseModel):
    act_work: str
    doel: DoelFRBR
    files: List[OwManifestBestand]


class OwManifestBuilder(OwFileBuilder):
    FILE_NAME = "manifest-ow.xml"
    TEMPLATE_PATH = "ow/manifest-ow.xml"

    def __init__(
        self,
        act_work: str,
        doel: DoelFRBR,
        manifest: List[OwManifestBestand],
    ):
        super().__init__()
        self._act_work = act_work
        self._doel = doel
        self._manifest = manifest

    def handle_ow_object_changes(self) -> None:
        # No changes made in manifest
        pass

    def build_template_data(self) -> OwManifestTemplateData:
        template_data = OwManifestTemplateData(act_work=self._act_work, doel=self._doel, files=self._manifest)
        self.template_data = template_data
        return template_data
