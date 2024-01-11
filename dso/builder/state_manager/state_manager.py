from typing import List

from .input_data.input_data_loader import InputData
from .models import OutputFile
from .states.artikel_eid_repository import ArtikelEidRepository
from .states.ow_repository import OWStateRepository


class StateManager:
    def __init__(self, input_data: InputData):
        self.input_data: InputData = input_data
        self.werkingsgebied_eid_lookup: dict = {}
        self.object_tekst_lookup: dict = {}
        self.artikel_eid: ArtikelEidRepository = ArtikelEidRepository()
        self.ow_repository: OWStateRepository = OWStateRepository()
        self._output_files: List[OutputFile] = []

    def add_output_file(self, output_file: OutputFile):
        self._output_files.append(output_file)

    def get_output_files(self) -> List[OutputFile]:
        output_files = sorted(self._output_files, key=lambda o: o.filename)
        return output_files

    def get_output_file_by_filename(self, filename: str) -> OutputFile:
        for output_file in self._output_files:
            if output_file.filename == filename:
                return output_file

        raise RuntimeError(f"Output file with filename {filename} not found")
