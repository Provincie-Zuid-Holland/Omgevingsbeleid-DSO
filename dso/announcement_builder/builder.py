import io
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile

from ..services.utils.os import empty_directory
from .builder_service import BuilderService
from .services.aanlevering_kennisgeving.aanlevering_kennisgeving_builder import AanleveringKennisgevingBuilder
from .services.lvbb.manifest_builder import ManifestBuilder
from .services.lvbb.opdracht_builder import OpdrachtBuilder
from .state_manager.models import InputData, StrContentData
from .state_manager.state_manager import StateManager


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)
        self._services: List[BuilderService] = [
            OpdrachtBuilder(),
            AanleveringKennisgevingBuilder(),
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

    def zip_files(self) -> io.BytesIO:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
            for output_file in self._state_manager.get_output_files():
                match output_file.content:
                    case StrContentData():
                        zip_file.writestr(output_file.filename, output_file.content.content)

        zip_buffer.seek(0)
        return zip_buffer
