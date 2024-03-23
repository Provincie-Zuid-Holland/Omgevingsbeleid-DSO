import io
from typing import Dict, List
from zipfile import ZIP_DEFLATED, ZipFile

from ..services.assets.create_image import create_image, create_image_in_zip
from ..services.utils.os import empty_directory
from .services import BuilderService
from .services.aanlevering_besluit.aanlevering_besluit_builder import AanleveringBesluitBuilder
from .services.asset.asset_builder import AssetBuilder
from .services.geo.geo_informatie_object_vaststelling_builder import GeoInformatieObjectVaststellingBuilder
from .services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from .services.lvbb.manifest_builder import ManifestBuilder
from .services.lvbb.opdracht_builder import OpdrachtBuilder
from .services.ow.ow_builder import OwBuilder
from .state_manager.input_data.input_data_loader import InputData
from .state_manager.models import AssetContentData, StrContentData
from .state_manager.state_manager import StateManager


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

    def zip_files(self) -> io.BytesIO:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
            for output_file in self._state_manager.get_output_files():
                match output_file.content:
                    case StrContentData():
                        zip_file.writestr(output_file.filename, output_file.content.content)

                    case AssetContentData():
                        create_image_in_zip(output_file.content.asset, zip_file, output_file.filename)

        zip_buffer.seek(0)
        return zip_buffer

    def export_json_state(self) -> str:
        """
        Export a JSON representation of the state to archive
        the inpurt/output of the builder and handle new objects created.
        """
        state = self._state_manager.build_state_export()
        return state.json()

    def get_used_wid_map(self) -> Dict[str, str]:
        return self._state_manager.get_used_wid_map()

    def get_used_wids(self) -> List[str]:
        return self._state_manager.get_used_wids()
