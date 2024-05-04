from typing import List, Optional

from ...services.ewid.ewid_service import EWIDService
from ..state_manager.states.artikel_eid_repository import ArtikelEidRepository
from ..state_manager.states.ow_repository import OWStateRepository
from .input_data.input_data_loader import InputData
from .models import OutputFile
from .states.artikel_eid_repository import ArtikelEidRepository
from .states.ow_repository import OWStateRepository


class StateManager:
    def __init__(self, input_data: InputData):
        self.input_data: InputData = input_data
        self.werkingsgebied_eid_lookup: dict = {}
        self.artikel_eid: ArtikelEidRepository = ArtikelEidRepository()
        self.ow_repository: OWStateRepository = OWStateRepository(input_data.ow_data)
        self.output_files: List[OutputFile] = []
        self.debug: dict = {}
        self.regeling_vrijetekst: Optional[str] = None

        # All OW IDS for export purposes
        self.created_ow_object_ids: List[str] = []
        # Mapping of created OW IDS to input identifiers for export state reference
        self.created_ow_objects_map: dict = {}

        # Service is in the state manager
        # As we use it on multiple places, and the internal state should be updates for each use
        # @note: act_ewid_service is used within:
        #           <RegelingVrijetekst componentnaam="nieuweregeling"
        self.act_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.publication_settings.provincie_id}_{input_data.publication_settings.regeling_frbr.Expression_Version}",
            known_wid_map=input_data.get_known_wid_map(),
            known_wids=input_data.get_known_wids(),
            werkingsgebied_repository=input_data.resources.werkingsgebied_repository,
        )
        self.bill_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.publication_settings.provincie_id}_{input_data.publication_settings.regeling_frbr.Expression_Version}",
        )

    def add_output_file(self, output_file: OutputFile):
        self.output_files.append(output_file)

    def get_output_files(self) -> List[OutputFile]:
        output_files = sorted(self.output_files, key=lambda o: o.filename)
        return output_files

    def get_output_file_by_filename(self, filename: str) -> OutputFile:
        for output_file in self.output_files:
            if output_file.filename == filename:
                return output_file

        raise RuntimeError(f"Output file with filename {filename} not found")
