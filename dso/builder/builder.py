import shutil
from typing import List

from dso.builder.services import BuilderService
from dso.builder.services.aanlevering_besluit.aanlevering_besluit_builder import AanleveringBesluitBuilder
from dso.builder.services.asset.asset_builder import AssetBuilder
from dso.builder.services.geo.geo_informatie_object_vaststelling_builder import GeoInformatieObjectVaststellingBuilder
from dso.builder.services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from dso.builder.services.lvbb.manifest_builder import ManifestBuilder
from dso.builder.services.lvbb.opdracht_builder import OpdrachtBuilder
from dso.builder.services.ow.ow_builder import OwBuilder
from dso.builder.state_manager.input_data.input_data_loader import InputData
from dso.builder.state_manager.models import AssetContentData, FileContentData, StrContentData
from dso.builder.state_manager.state_manager import StateManager
from dso.services.assets.create_image import create_image
from dso.services.utils.os import empty_directory


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)
        self._services: List[BuilderService] = [
            OpdrachtBuilder(),
            AanleveringBesluitBuilder(),
            OwBuilder(),
            GeoInformatieObjectVaststellingBuilder(),
            GioAanleveringInformatieObjectBuilder(),
            AssetBuilder(),
            ManifestBuilder(),
        ]

    def build_publication_files(self):
        for service in self._services:
            self._state_manager = service.apply(self._state_manager)

    def save_files(self, output_dir: str):
        empty_directory(output_dir)

        for output_file in self._state_manager.get_output_files():
            destination_path = f"{output_dir}/{output_file.filename}"
            match output_file.content:
                case StrContentData():
                    with open(destination_path, "w") as f:
                        f.write(output_file.content.content)

                case AssetContentData():
                    create_image(output_file.content.asset, destination_path)

                case FileContentData():
                    shutil.copy2(output_file.content.source_path, destination_path)
